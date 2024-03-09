import os
import dotenv
import bs4
import pickle
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores.redis import Redis
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Cohere
from langchain_community.embeddings import CohereEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel
from langchain_community.document_loaders import PyPDFLoader

dotenv.load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def initialize_database():
    embedding = CohereEmbeddings()
    redis_index = "hackHer"
    if os.path.isfile("vectorstore.pkl"):
        with open("vectorstore.pkl", "rb") as f:
            schema, key_prefix = pickle.load(f)
        vectorstore = Redis.from_existing_index(embedding=embedding, index_name=redis_index, schema=schema,
                                                key_prefix=key_prefix, redis_url=REDIS_URL)
        print("Loaded existing vectorstore from file.")
    else:
        loader = PyPDFLoader("Guidelines-FINAL-4TH-EDITION-With-2023-Updates.pdf")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Redis.from_documents(documents=splits, embedding=CohereEmbeddings(), redis_url=REDIS_URL)
        with open("vectorstore.pkl", "wb") as f:
            pickle.dump([vectorstore.schema, vectorstore.key_prefix], f)
        print("Created new vectorstore from file.")
    return vectorstore


def rag_chain_invoke(vectorstore, question):
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    llm = Cohere()

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


vectorstore = initialize_database()
print(rag_chain_invoke(vectorstore, "What is the Gender-affirming care?"))
