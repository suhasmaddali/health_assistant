import langchain
import streamlit as st
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models import ChatOpenAI
from langchain.cache import InMemoryCache
from langchain.prompts import PromptTemplate

langchain.llm_cache = InMemoryCache()

load_dotenv()

import warnings
warnings.filterwarnings("ignore")

chat = ChatOpenAI()

system_message = """You are a helpful doctor who answers all the queries like a doctor. 
Ensure to give a {detail} nutrition plan for your application and useful piece of advice as a doctor to the person. 
Ensure that you are optimistic and give encouraging words to patient regarding their health. Also {medication} give medication if necessary if the patient needs to improve their condition.
As a doctor, do not answer any other questions not pertaining to your occupation."""

system_message_prompt = PromptTemplate(
    input_variables=['detail', 'medication'],
    template=system_message
)

st.set_page_config(page_title="Health Assistant", page_icon=":robot:")
st.header("Hello there, I'm your Health Assistant.") 

if "sessionMessages" not in st.session_state:
    st.session_state.sessionMessages = [
        SystemMessage(content=system_message_prompt.format(detail='highest', medication='yes'))
    ]

def load_answer(question):
    st.session_state.sessionMessages.append(HumanMessage(content=question))
    assistant_answer = chat(st.session_state.sessionMessages)
    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
    return assistant_answer.content

def get_text():
    input_text = st.text_input("You: ", key=input)
    return input_text

user_input = get_text()
submit = st.button("Advice")

if submit and user_input:
    with st.spinner("Generating response..."):
        response = load_answer(user_input)

# Display all messages and add TTS for AI Messages
for idx, message in enumerate(st.session_state.sessionMessages):
    if isinstance(message, HumanMessage):
        st.markdown(f'<span style="color:green">**You:**</span> \n\n{message.content}', unsafe_allow_html=True)
    elif isinstance(message, AIMessage):
        st.markdown(f'<span style="color:#ffd700">**Assistant:**</span> \n\n{message.content}', unsafe_allow_html=True)
