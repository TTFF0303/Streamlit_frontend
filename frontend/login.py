"""
Login module for the AI Assistant application.
Handles user authentication and login page rendering.
"""

import streamlit as st
import logging

# Get the logger from the main app
logger = logging.getLogger(__name__)

def login_page():
    """
    Render the login page for user authentication.
    
    This function displays a login form with username and password fields.
    Upon submission, it validates the credentials (mock validation in this case)
    and sets the session state to indicate the user is logged in.
    """
    logger.info("Rendering login page")
    st.title("AI Assistant Login")
    
    # Create a form for login
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            # Simple authentication (in real app, you would verify credentials against a database)
            if username and password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                logger.info(f"User {username} logged in successfully")
                st.rerun()
            else:
                st.error("Please enter both username and password")
                logger.warning("Login attempt with missing credentials")
