import streamlit as st
import requests
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException 
from app.backend import api 

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent", layout="centered")
st.title("Multi AI Agent Using Groq and Tavily")

system_prompt = st.text_area("Define your AI Agent", height=300)
selected_model = st.selectbox("Select your AI Model", settings.ALLOWED_MODEL_NAMES)
allow_web_search = st.checkbox("Allow Web Search")
user_query = st.text_area("User Query", height=100) 
API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
                    "model_name" : selected_model,
                    "system_prompt" : system_prompt, 
                    "messages" : [user_query], 
                    "allow_search" : allow_web_search
    }

    try:
        logger.info(f"Sending the request to backend")
        response = requests.post(API_URL, json = payload) 
        
        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info(f"Received response from backend: {agent_response}")
            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html = True) 
            
        else:
            logger.error("Backend Error") 
            st.error("Error with Backend")
            
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        st.error("An error occurred while processing your request. Please try again later.")
        raise CustomException("An error occurred while processing your request.") from e