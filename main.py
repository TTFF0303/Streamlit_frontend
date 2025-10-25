"""
Main application file for the AI Assistant.
This file orchestrates the application flow and imports UI components from the frontend module.
"""

import streamlit as st
import logging
import os
from dotenv import load_dotenv

# Import frontend components
from frontend.login import login_page
from frontend.interface import render_sidebar, render_chat_interface, render_metrics_interface, render_history_interface

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Mock API key for local testing
MOCK_API_KEY = "sk-mock-api-key-for-local-testing"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "GPT-4"  # Default model
    
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "English"  # Default language
    
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", MOCK_API_KEY)

def main_app():
    """
    Render the main application interface.
    
    This function orchestrates the main app by:
    1. Rendering the sidebar
    2. Determining which view to display based on session state
    3. Calling the appropriate render function for the selected view
    """
    logger.info("Rendering main application interface")
    
    # Render the sidebar
    render_sidebar()
    
    # Main content area
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "chat"
        
    if st.session_state.current_view == "chat":
        render_chat_interface()
    elif st.session_state.current_view == "metrics":
        render_metrics_interface()
    elif st.session_state.current_view == "history":
        render_history_interface()

def main():
    """
    Main application entry point.
    
    This function determines whether to show the login page or the main app
    based on the user's authentication status.
    """
    logger.info("Starting AI Assistant application")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
