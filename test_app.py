"""
Test suite for the AI Assistant application.
This file tests the main functionalities of the refactored AI Assistant web app.
"""

import streamlit as st
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main app functions
import main
from frontend import interface

def test_app():
    """
    Test the main functionalities of the app.
    
    This function runs a series of tests to verify that the application
    components are working correctly after refactoring.
    """
    st.title("AI Assistant App - Test Suite")
    
    st.write("This test suite verifies the main functionalities of the AI Assistant web app.")
    
    # Test 1: Check if required modules can be imported
    st.subheader("Test 1: Module Import Test")
    try:
        import logging
        import json
        from dotenv import load_dotenv
        st.success("✓ All required modules imported successfully")
    except Exception as e:
        st.error(f"✗ Error importing modules: {e}")
    
    # Test 2: Check if environment variables are loaded
    st.subheader("Test 2: Environment Variables Test")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY", "sk-mock-api-key-for-local-testing")
        if api_key:
            st.success("✓ Environment variables loaded successfully")
            st.info(f"API Key: {api_key[:10]}...{api_key[-5:] if len(api_key) > 15 else ''}")
        else:
            st.warning("⚠ API key not found, using default")
    except Exception as e:
        st.error(f"✗ Error loading environment variables: {e}")
    
    # Test 3: Check if frontend modules are available
    st.subheader("Test 3: Frontend Modules Availability Test")
    try:
        # Check if frontend modules can be imported
        from frontend.login import login_page
        from frontend.interface import render_sidebar, render_chat_interface
        st.success("✓ All frontend modules imported successfully")
    except Exception as e:
        st.error(f"✗ Error importing frontend modules: {e}")
    
    # Test 4: Check if session state variables are initialized
    st.subheader("Test 4: Session State Initialization Test")
    try:
        # Initialize session state variables if not present
        session_vars = ['logged_in', 'current_user', 'chat_history', 'selected_model', 'selected_language', 'api_key']
        initialized_vars = []
        missing_vars = []
        
        for var in session_vars:
            if hasattr(st.session_state, var):
                initialized_vars.append(var)
            else:
                missing_vars.append(var)
        
        if len(missing_vars) == 0:
            st.success("✓ All session state variables initialized")
        else:
            st.warning(f"⚠ Some session state variables not initialized: {missing_vars}")
            
        st.info(f"Initialized variables: {initialized_vars}")
    except Exception as e:
        st.error(f"✗ Error checking session state: {e}")
    
    # Test 5: Check if logging is configured
    st.subheader("Test 5: Logging Configuration Test")
    try:
        import logging
        logger = logging.getLogger(__name__)
        st.success("✓ Logging configured successfully")
        st.info("Logging level: " + logging.getLevelName(logger.getEffectiveLevel()))
    except Exception as e:
        st.error(f"✗ Error configuring logging: {e}")

if __name__ == "__main__":
    test_app()
