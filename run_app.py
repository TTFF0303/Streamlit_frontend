#!/usr/bin/env python3
"""
Startup script for the AI Assistant Streamlit application.
This script sets up the environment and runs the main application.
"""

import os
import sys
import subprocess
import logging

def setup_logging():
    """
    Set up basic logging configuration.
    
    This function configures the logging system to write to both a file
    and the console, which is useful for debugging and monitoring the
    application's behavior.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def check_dependencies():
    """
    Check if required dependencies are installed.
    
    This function verifies that all required Python packages are available
    before attempting to run the application. This helps prevent runtime
    errors due to missing dependencies.
    """
    try:
        import streamlit
        import openai
        import pandas
        import dotenv
        return True
    except ImportError as e:
        logger.error(f"Missing required dependency: {e}")
        return False

def load_environment():
    """
    Load environment variables from .env file.
    
    This function loads environment variables from the .env file in the
    project root directory, which is useful for configuration and
    sensitive information like API keys.
    """
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment variables loaded")

def run_streamlit():
    """
    Run the Streamlit application.
    
    This function starts the Streamlit development server with the main
    application file. It handles common errors like Streamlit not being
    installed or issues with running the application.
    """
    try:
        # Run streamlit with the main app file
        subprocess.run(["streamlit", "run", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Streamlit app: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logger.error("Streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    # Set up logging
    logger = setup_logging()
    logger.info("Starting AI Assistant application")
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Dependencies check failed. Please install required packages.")
        sys.exit(1)
    
    # Load environment variables
    load_environment()
    
    # Run the Streamlit app
    run_streamlit()
