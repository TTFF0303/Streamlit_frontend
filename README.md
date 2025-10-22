# AI Assistant Web App

This is a Streamlit-based web application that serves as a frontend for an AI assistant with BI capabilities. It can be deployed to Azure Web App.

## Features

1. Login page for user authentication
2. Chat interface for interacting with the AI assistant
3. Model selection (GPT-4, GPT-3.5, Claude-2)
4. Language selection (English, Chinese)
5. Chat history management
6. Related questions generation after each response
7. Attribution analysis and data drill-down capabilities
8. Metrics definition interface for translating natural language to SQL
9. Comprehensive logging for debugging
10. Mock data for local testing

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the source code
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application Locally

1. Navigate to the project directory
2. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

3. The application will open in your default web browser. If it doesn't, visit `http://localhost:8501` in your browser.

## Deployment Options

### Azure Web App Deployment

1. Create an Azure Web App
2. Configure the web app to use Python
3. Deploy the application files to the web app
4. Set the startup command to:
   ```bash
   python -m streamlit run main.py --server.port 8000 --server.address 0.0.0.0
   ```
5. Add the application settings in Azure:
   - `SCM_DO_BUILD_DURING_DEPLOYMENT`: true

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t ai-assistant-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 ai-assistant-app
   ```

3. Access the application at `http://localhost:8501`

### GitHub Actions Deployment

The project includes a GitHub Actions workflow file (`azure-deploy.yaml`) for automated deployment to Azure Web App. To use it:

1. Fork this repository
2. Set up the required secrets in your GitHub repository:
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: Your Azure Web App publish profile
3. Push changes to the `main` branch to trigger the deployment workflow

## Configuration

The application uses the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (for production use)

For local testing, a mock API key is provided in the `.env` file.

## Logging

The application logs to both a file (`app.log`) and the console. Logs include:
- User login/logout events
- API key updates
- User messages
- System events

## File Structure

```
.
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (for local testing)
├── app.log              # Log file (created when the app runs)
└── README.md            # This file
```

## Customization

To customize the application:

1. Modify the `MOCK_DATA` dictionary in `main.py` to change the sample metrics, models, and languages
2. Update the UI components in the respective render functions
3. Add new features by extending the session state variables and UI components

## Troubleshooting

If you encounter issues:

1. Check the logs in `app.log` for error messages
2. Ensure all dependencies are installed correctly
3. Verify the environment variables are set correctly
4. Check that the required ports are available

## License

This project is licensed under the MIT License.
