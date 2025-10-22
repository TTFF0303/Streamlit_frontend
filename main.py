import streamlit as st
import logging
import json
from datetime import datetime
import os
from dotenv import load_dotenv

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

# Mock data and API keys for local testing
MOCK_API_KEY = "sk-mock-api-key-for-local-testing"
MOCK_DATA = {
    "metrics": [
        {"id": 1, "name": "Revenue", "description": "Total revenue generated"},
        {"id": 2, "name": "User Count", "description": "Number of active users"},
        {"id": 3, "name": "Conversion Rate", "description": "Percentage of visitors who convert"}
    ],
    "models": ["GPT-4", "GPT-3.5", "Claude-2"],
    "languages": ["English", "Chinese"],
    "sample_chats": [
        {"role": "user", "content": "Show me revenue trends"},
        {"role": "assistant", "content": "Here are the revenue trends for the last quarter...", "related_questions": [
            "What factors contributed to the revenue increase?",
            "How does this compare to the previous quarter?",
            "Which regions showed the highest growth?"
        ], "attribution": "Based on Q3 financial reports", "drill_down_data": "Revenue by region: North America: $2M, Europe: $1.5M, Asia: $1M"}
    ]
}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = MOCK_DATA["models"][0]
    
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = MOCK_DATA["languages"][0]
    
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", MOCK_API_KEY)

def login_page():
    """Render the login page"""
    logger.info("Rendering login page")
    st.title("AI Assistant Login")
    
    # Create a form for login
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            # Simple authentication (in real app, you would verify credentials)
            if username and password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                logger.info(f"User {username} logged in successfully")
                st.rerun()
            else:
                st.error("Please enter both username and password")
                logger.warning("Login attempt with missing credentials")

def main_app():
    """Render the main application interface"""
    logger.info("Rendering main application interface")
    
    # Sidebar for settings and navigation
    with st.sidebar:
        st.title("Settings")
        
        # User info and logout
        st.write(f"Welcome, {st.session_state.current_user}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.chat_history = []
            logger.info("User logged out")
            st.rerun()
            
        # Model selection
        st.subheader("Model Selection")
        selected_model = st.selectbox(
            "Choose Model:",
            MOCK_DATA["models"],
            index=MOCK_DATA["models"].index(st.session_state.selected_model) if st.session_state.selected_model in MOCK_DATA["models"] else 0
        )
        st.session_state.selected_model = selected_model
        
        # Language selection
        st.subheader("Language")
        selected_language = st.radio(
            "Choose Language:",
            MOCK_DATA["languages"],
            index=MOCK_DATA["languages"].index(st.session_state.selected_language) if st.session_state.selected_language in MOCK_DATA["languages"] else 0
        )
        st.session_state.selected_language = selected_language
        
        # Navigation buttons
        st.subheader("Navigation")
        if st.button("Chat Interface"):
            st.session_state.current_view = "chat"
        if st.button("Metrics Definition"):
            st.session_state.current_view = "metrics"
        if st.button("History"):
            st.session_state.current_view = "history"
            
        # API Key input
        st.subheader("API Configuration")
        api_key = st.text_input("API Key:", value=st.session_state.api_key, type="password")
        if st.button("Update API Key"):
            st.session_state.api_key = api_key
            st.success("API Key updated!")
            logger.info("API key updated")

    # Main content area
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "chat"
        
    if st.session_state.current_view == "chat":
        render_chat_interface()
    elif st.session_state.current_view == "metrics":
        render_metrics_interface()
    elif st.session_state.current_view == "history":
        render_history_interface()

def render_chat_interface():
    """Render the chat interface"""
    logger.info("Rendering chat interface")
    st.title("AI Assistant Chat")
    
    # Display welcome message if chat history is empty
    if not st.session_state.chat_history:
        with st.chat_message("assistant"):
            welcome_message = "Hello! I'm your AI assistant. How can I help you today?"
            st.markdown(welcome_message)
            
            # Add welcome message to chat history
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": welcome_message,
                "related_questions": [
                    "What can you help me with?",
                    "How do I use this application?",
                    "What metrics can I analyze?"
                ],
                "attribution": "Default welcome message",
                "drill_down_data": "Welcome to the AI Assistant application"
            })
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # If it's an assistant message, show additional features
            if message["role"] == "assistant" and "related_questions" in message:
                # Show related questions
                st.subheader("Related Questions:")
                cols = st.columns(3)
                for i, question in enumerate(message["related_questions"]):
                    if i < 3:  # Limit to 3 questions
                        with cols[i]:
                            if st.button(question, key=f"related_{len(st.session_state.chat_history)}_{i}"):
                                # Add the related question to the chat
                                st.session_state.chat_history.append({"role": "user", "content": question})
                                # Generate mock response
                                mock_response = f"This is a response to your related question: {question}"
                                st.session_state.chat_history.append({
                                    "role": "assistant", 
                                    "content": mock_response,
                                    "related_questions": [
                                        f"What about the {['impact', 'trends', 'details'][i % 3]} of this?",
                                        f"How does this relate to {['revenue', 'users', 'growth'][i % 3]}?",
                                        f"Can you {['explain', 'analyze', 'compare'][i % 3]} this further?"
                                    ],
                                    "attribution": f"Based on mock data for '{question}'",
                                    "drill_down_data": "Mock drill-down data would appear here"
                                })
                                st.rerun()
                
                # Show attribution and drill-down buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Attribution Analysis", key=f"attr_{len(st.session_state.chat_history)}"):
                        st.info(message.get("attribution", "No attribution data available"))
                        
                with col2:
                    if st.button("Data Drill-down", key=f"drill_{len(st.session_state.chat_history)}"):
                        st.info(message.get("drill_down_data", "No drill-down data available"))

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        logger.info(f"User message: {prompt}")
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Generate mock AI response
        with st.chat_message("assistant"):
            # Simulate processing
            response = f"I understand you're asking about '{prompt}'. This is a mock response from the AI assistant."
            
            # Add response to history with additional features
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": response,
                "related_questions": [
                    f"What are the key factors affecting {prompt}?",
                    f"How has {prompt} changed over time?",
                    f"What are the implications of {prompt} for our business?"
                ],
                "attribution": f"Based on mock analysis of '{prompt}'",
                "drill_down_data": "Mock data drill-down: Detailed analysis would appear here with charts and tables"
            })
            
            st.markdown(response)
            
            # Show related questions
            st.subheader("Related Questions:")
            cols = st.columns(3)
            for i, question in enumerate([
                f"What are the key factors affecting {prompt}?",
                f"How has {prompt} changed over time?",
                f"What are the implications of {prompt} for our business?"
            ]):
                if i < 3:  # Limit to 3 questions
                    with cols[i]:
                        if st.button(question, key=f"related_new_{i}"):
                            # Add the related question to the chat
                            st.session_state.chat_history.append({"role": "user", "content": question})
                            # Generate mock response
                            mock_response = f"This is a response to your related question: {question}"
                            st.session_state.chat_history.append({
                                "role": "assistant", 
                                "content": mock_response,
                                "related_questions": [
                                    f"What about the {['impact', 'trends', 'details'][i % 3]} of this?",
                                    f"How does this relate to {['revenue', 'users', 'growth'][i % 3]}?",
                                    f"Can you {['explain', 'analyze', 'compare'][i % 3]} this further?"
                                ],
                                "attribution": f"Based on mock data for '{question}'",
                                "drill_down_data": "Mock drill-down data would appear here"
                            })
                            st.rerun()

def render_metrics_interface():
    """Render the metrics definition interface"""
    logger.info("Rendering metrics interface")
    st.title("Metrics Definition")
    
    st.write("Define metrics that the AI can recognize and translate to SQL queries.")
    
    # Display existing metrics
    st.subheader("Existing Metrics")
    for metric in MOCK_DATA["metrics"]:
        with st.expander(metric["name"]):
            st.write(f"ID: {metric['id']}")
            st.write(f"Description: {metric['description']}")
            st.code(f"SELECT * FROM metrics WHERE id = {metric['id']}; -- Mock SQL query", language="sql")
    
    # Add new metric form
    st.subheader("Add New Metric")
    with st.form("new_metric_form"):
        metric_name = st.text_input("Metric Name")
        metric_description = st.text_area("Description")
        sample_sql = st.text_area("Sample SQL Query", placeholder="SELECT * FROM table WHERE condition;")
        submitted = st.form_submit_button("Add Metric")
        
        if submitted:
            if metric_name and metric_description and sample_sql:
                new_metric = {
                    "id": len(MOCK_DATA["metrics"]) + 1,
                    "name": metric_name,
                    "description": metric_description
                }
                MOCK_DATA["metrics"].append(new_metric)
                st.success(f"Added new metric: {metric_name}")
                logger.info(f"New metric added: {metric_name}")
                st.rerun()
            else:
                st.error("Please fill in all fields")

def render_history_interface():
    """Render the chat history interface"""
    logger.info("Rendering history interface")
    st.title("Chat History")
    
    if st.session_state.chat_history:
        # Group messages by date
        grouped_history = {}
        for message in st.session_state.chat_history:
            # For simplicity, we'll group by session (all messages together)
            # In a real app, you might group by actual dates
            date_key = "Current Session"
            if date_key not in grouped_history:
                grouped_history[date_key] = []
            grouped_history[date_key].append(message)
        
        # Display history
        for date, messages in grouped_history.items():
            with st.expander(date, expanded=True):
                for message in messages:
                    role = message["role"]
                    content = message["content"]
                    st.markdown(f"**{role.capitalize()}:** {content}")
                    
        # Clear history button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            logger.info("Chat history cleared")
            st.success("Chat history cleared!")
            st.rerun()
    else:
        st.info("No chat history yet. Start a conversation!")

def main():
    """Main application entry point"""
    logger.info("Starting AI Assistant application")
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
