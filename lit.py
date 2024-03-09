from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory
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


# https://stackoverflow.com/questions/74003574/how-to-create-a-button-with-hyperlink-in-streamlit
def redirect_button(url: str, text: str = None, color="#FD504D"):
    st.markdown(
        f"""
    <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
        unsafe_allow_html=True
    )


def format_response(input):
    output = ""
    output += input['answer']
    output += "\n\n Sources: \n"
    # Extract sources and pages
    sources_pages = [(doc.metadata['source'], doc.metadata['page']) for doc in input['context']]

    # Format and print
    for source, page in sources_pages:
        output += f"- {source} - Page {page} \n"
    return output


st.set_page_config(page_title="hackHer", page_icon="🌸")

redirect_button("https://owl.purdue.edu/owl/research_and_citation/apa_style/apa_formatting_and_style_guide/index.html","Take me to safety!")

vectorstore = initialize_database()

msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
)

if len(msgs.messages) == 0:
    msgs.clear()
    msgs.add_ai_message("How can I help you?")

avatars = {"human": "🌷", "ai": "🌺"}
for idx, msg in enumerate(msgs.messages):
    with st.chat_message(avatars[msg.type]):
        st.write(msg.content)

if prompt := st.chat_input():
    st.chat_message("🌷").write(prompt)
    msgs.add_user_message(prompt)

    with st.chat_message("🌺"):
        response = rag_chain_invoke(vectorstore, prompt)
        formatted_response = format_response(response)
        st.markdown(formatted_response)
        msgs.add_ai_message(formatted_response)
