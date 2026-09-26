# Trello to Markdown Exporter

This is a Streamlit web application for exporting Trello boards to a detailed markdown file.

## Features

*   Connects to your Trello account using your API key and token.
*   Password protected access to the application.
*   Lists your available workspaces and boards.
*   Filters for open boards and lists, ignoring closed/archived ones.
*   Generates a comprehensive markdown file that includes:
    *   Board and list names.
    *   Card details (description, labels, dates, etc.).
    *   Checklists with their completion status.
    *   Card comments.
    *   Image attachments.
*   Provides a real-time progress indicator during the export process.
*   Allows you to download the generated markdown file.

## How to Run in Firebase Studio

1.  **Set up your environment:**
    *   Create a `.env` file in the root of the project.
    *   Add your Trello API key, token and app password to the `.env` file:
        ```
        TRELLO_API_KEY="your_api_key"
        TRELLO_API_TOKEN="your_api_token"
        APP_PASSWORD="your_app_password"
        ```
2.  **Install dependencies:**
    *   Open the terminal in Firebase Studio.
    *   Run `pip install -r requirements.txt`.
3.  **Start the application:**
    *   In the terminal, run the command: `streamlit run app.py`
    *   The application will be available in the web preview panel.

## Deployed Service URL

https://idx-trello-md-v4-09031501-17999627323.europe-west4.run.app
