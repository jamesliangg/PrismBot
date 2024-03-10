import os
import dotenv
import pickle
import argparse
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores.redis import Redis
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
# from langchain_community.llms import Cohere
# from langchain_community.embeddings import CohereEmbeddings

dotenv.load_dotenv()

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def initialize_database():
    # embedding = CohereEmbeddings()
    embedding = VertexAIEmbeddings(model_name="textembedding-gecko@001")
    if os.path.isfile("vectorstore.pkl"):
        with open("vectorstore.pkl", "rb") as f:
            schema, key_prefix, index_name = pickle.load(f)
        vectorstore = Redis.from_existing_index(embedding=embedding, index_name=index_name, schema=schema,
                                                key_prefix=key_prefix, redis_url=REDIS_URL)
        print("Loaded existing vectorstore from file.")
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.5060.114 Safari/537.36'}
        loader = PyPDFLoader(file_path="https://www.rainbowhealthontario.ca/wp-content/uploads/2021/09/Guidelines"
                                       "-FINAL-4TH-EDITION-With-2023-Updates.pdf", headers=headers)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Redis.from_documents(documents=splits, embedding=embedding, redis_url=REDIS_URL)
        with open("vectorstore.pkl", "wb") as f:
            pickle.dump([vectorstore.schema, vectorstore.key_prefix, vectorstore.index_name], f)
        print("Created new vectorstore from file.")
    return vectorstore


def rag_chain_invoke(vectorstore, question):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    prompt = hub.pull("rlm/rag-prompt")
    # llm = Cohere()
    llm = VertexAI(model_name="gemini-pro")

    rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | prompt
            | llm
            | StrOutputParser()
    )
    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)
    return rag_chain_with_source.invoke(question)


def add_documents_web(vectorstore, url):
    is_pdf = is_pdf_url(url)
    if is_pdf:
        print("Parsing PDF")
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.5060.114 Safari/537.36'}
        loader = PyPDFLoader(
            file_path=url,
            headers=headers)
        docs = loader.load()
    else:
        print("Parsing website")
        docs = parse_website(url)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    # vectorstore.add_documents(documents=splits, embedding=CohereEmbeddings(), redis_url=REDIS_URL)
    vectorstore.add_documents(documents=splits, embedding=VertexAIEmbeddings(model_name="textembedding-gecko@001"),
                              redis_url=REDIS_URL)
    print(url)
    return "Successfully added documents to database."


def parse_website(url):
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("page-content", "page-title-bar", "title-header", "post-content")
            )
        ),
    )
    return loader.load()


def is_pdf_url(url):
    return url.lower().endswith('.pdf')


if __name__ == "__main__":
    parser = argparse.ArgumentParser("add_to_database")
    parser.add_argument("url", help="URL of document to add to database", type=str)
    args = parser.parse_args()
    vectorstore = initialize_database()
    add_documents_web(vectorstore, args.url)
    # print(is_pdf_url(args.url))
    # print(parse_website(args.url))
    # print(args.url)
    # add_documents_web(vectorstore, args.url)
