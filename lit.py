from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
import streamlit as st
from chat import rag_chain_invoke, initialize_database


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


def format_response(input):
    output = ""
    output += input['answer']
    output += "\n\n Sources: \n\n"
    # Extract sources and pages
    sources_pages = [(doc.metadata['source'], doc.metadata['page']) for doc in input['context']]

    # Format and print
    for source, page in sources_pages:
        output += f"{source} - Page {page} \n"
    return output


vectorstore = initialize_database()

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    # with st.chat_message("assistant"):
    #     # stream_handler = StreamHandler(st.empty())
    #     # llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
    #     # response = llm.invoke(st.session_state.messages)
    #     # response = rag_chain_invoke(vectorstore, prompt, stream_handler)
    #     response = rag_chain_invoke(vectorstore, prompt)
    #     print(response)
    #     formatted_response = format_response(response)
    #     st.session_state.messages.append(ChatMessage(role="assistant", content=str(response)))
    #     st.chat_message("assistant").write(formatted_response)
    response = rag_chain_invoke(vectorstore, prompt)
    # print(response)
    formatted_response = format_response(response)
    st.chat_message("assistant").write(formatted_response)
