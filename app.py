import streamlit as st
from langchain.prompts import PromptTemplate
import requests

import warnings
warnings.filterwarnings("ignore")

def chatmixtral(message_dict):

    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/8f4118ba-60a8-4e6b-8574-e38a4067a4a3"
    fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"
    
    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/json",
    }
    
    payload = {
      "messages": message_dict,
      "temperature": 0.2,
      "top_p": 0.7,
      "max_tokens": 1024,
      "seed": 42,
      "stream": False
    }
    
    # re-use connections
    session = requests.Session()
    
    response = session.post(invoke_url, headers=headers, json=payload)
    
    while response.status_code == 202:
        request_id = response.headers.get("NVCF-REQID")
        fetch_url = fetch_url_format + request_id
        response = session.get(fetch_url, headers=headers)
    
    response.raise_for_status()
    response_body = response.json()
    return response_body['choices'][0]['message']

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
        {
            'content': system_message_prompt.format(detail='highest', medication='yes'),
            'role': 'system'
        }
    ]

def load_answer(question):
    human_message_dict = {
        'content': question,
        'role': 'user'
    }
    st.session_state.sessionMessages.append(human_message_dict)
    assistant_answer = chatmixtral(st.session_state.sessionMessages)
    st.session_state.sessionMessages.append(assistant_answer)
    return assistant_answer

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
    if idx == 0:
        continue
    if idx == 1:
        continue
    if message['role'] == 'user':
        st.markdown(f'<span style="color:green">**You:**</span> \n\n{message["content"]}', unsafe_allow_html=True)
    else:
        st.markdown(f'<span style="color:#ffd700">**Assistant:**</span> \n\n{message["content"]}', unsafe_allow_html=True)


