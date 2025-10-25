#!/usr/bin/env python3
"""
Verification script for the AI Assistant Streamlit application.
This script checks if all required files are present and dependencies are installed.
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
    verification process.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("verification.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def check_required_files():
    """
    Check if all required files are present.
    
    This function verifies that all necessary files for the application
    are present in the project directory, including the new frontend
    directory and its files.
    """
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        ".env",
        "test_app.py",
        "azure-deploy.yaml",
        "Dockerfile",
        ".dockerignore",
        "run_app.py",
        "verify_setup.py",
        "frontend/login.py",
        "frontend/interface.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            logger.error(f"Missing required file: {file}")
        else:
            logger.info(f"Found required file: {file}")
    
    return len(missing_files) == 0

def check_dependencies():
    """
    Check if required dependencies are installed.
    
    This function verifies that all required Python packages are available
    for the application to run properly.
    """
    required_packages = [
        "streamlit",
        "openai",
        "pandas",
        "dotenv",
        "logging"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"Found required package: {package}")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"Missing required package: {package}")
    
    return len(missing_packages) == 0

def check_python_version():
    """
    Check if Python version is compatible.
    
    This function ensures that the Python version meets the minimum
    requirements for the application (Python 3.7+).
    """
    version_info = sys.version_info
    if version_info.major >= 3 and version_info.minor >= 7:
        logger.info(f"Python version {version_info.major}.{version_info.minor}.{version_info.micro} is compatible")
        return True
    else:
        logger.error(f"Python version {version_info.major}.{version_info.minor}.{version_info.micro} is not compatible. Required: Python 3.7+")
        return False

def check_streamlit():
    """
    Check if Streamlit is installed and working.
    
    This function verifies that Streamlit is properly installed and
    can be executed, which is essential for running the application.
    """
    try:
        result = subprocess.run(["streamlit", "--version"], capture_output=True, text=True, check=True)
        logger.info(f"Streamlit is installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Streamlit is not installed or not working properly")
        return False

def main():
    """
    Main verification function.
    
    This function orchestrates the verification process by running all
    checks and providing a summary of the results.
    """
    logger.info("Starting AI Assistant application verification")
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check required files
    files_ok = check_required_files()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check Streamlit
    streamlit_ok = check_streamlit()
    
    # Summary
    logger.info("=== Verification Summary ===")
    logger.info(f"Python version: {'OK' if python_ok else 'FAILED'}")
    logger.info(f"Required files: {'OK' if files_ok else 'FAILED'}")
    logger.info(f"Dependencies: {'OK' if deps_ok else 'FAILED'}")
    logger.info(f"Streamlit: {'OK' if streamlit_ok else 'FAILED'}")
    
    overall_status = python_ok and files_ok and deps_ok and streamlit_ok
    logger.info(f"Overall status: {'PASSED' if overall_status else 'FAILED'}")
    
    if overall_status:
        logger.info("✅ All checks passed! You can run the application with 'streamlit run main.py'")
    else:
        logger.error("❌ Some checks failed. Please review the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    logger = setup_logging()
    main()
