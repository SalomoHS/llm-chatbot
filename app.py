import streamlit as st
import requests
import time

# if "model" not in st.session_state:
#         st.session_state["model"] = gemini(GEMINI_API_KEY)
        
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi"}]

if "account_id" not in st.session_state:
    st.session_state.account_id = None

if "api_token" not in st.session_state:
    st.session_state.api_token = None

if "model_name" not in st.session_state:
    st.session_state.model_name = None

with st.sidebar:
    st.session_state.account_id  = st.text_input("Cloudflare Account ID")
    st.session_state.api_token = st.text_input("Cloudflare API") 
    st.session_state.model_name =  st.text_input("Model Name")

    api = f"https://api.cloudflare.com/client/v4/accounts/{st.session_state.account_id}/ai/run/"
    headers = {"Authorization": f"Bearer {st.session_state.api_token}"}

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    if (not st.session_state.account_id) and (not st.session_state.api_token) and (not st.session_state.model_name):
        st.info("Please add your API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
            st.markdown(prompt)
    
    chat_placeholder = st.empty()

    with chat_placeholder:
        st.write("🤔 Thinking...")
        payload = { "messages": st.session_state.messages , 'raw':'true'}
        response = requests.post(f"{api}{st.session_state.model_name}", headers=headers, json = payload, stream=True)
        st.empty()
    
    with st.chat_message("assistant"):  
        # st.write_stream(response)
        output = response.json()
        st.write_stream(stream_data(output['result']['response'].strip()))
        
        # st.markdown(output['result']['response'].strip())
    st.session_state.messages.append({"role": "assistant", "content": output['result']['response'].strip()})