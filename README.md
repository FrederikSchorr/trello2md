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

## How to Run in GitHub Codespaces (recommended)

This repo is set up with a devcontainer, so it needs no local setup.

1.  **Set your secrets** (once, before the first run):
    *   On GitHub, go to this repo → **Settings → Secrets and variables → Codespaces**.
    *   Add three repository secrets: `TRELLO_API_KEY`, `TRELLO_API_TOKEN`, `APP_PASSWORD`.
2.  **Start a Codespace:**
    *   On the repo's main page, click **Code → Codespaces → Create codespace on main**.
    *   Wait for the container to build (installs `requirements.txt` automatically) and for Streamlit to start.
    *   A "Ports" notification/preview opens automatically on port `8501` — that's the app.
3.  **When done:**
    *   Close the browser tab. Codespaces stop automatically after a period of inactivity, and the free tier (60 core-hours/month on personal accounts) comfortably covers occasional use.
    *   You can delete the codespace afterwards under **github.com/codespaces** if you don't plan to reuse it.

## Running locally (alternative)

1.  Create a `.env` file in the project root:
    ```
    TRELLO_API_KEY="your_api_key"
    TRELLO_API_TOKEN="your_api_token"
    APP_PASSWORD="your_app_password"
    ```
2.  `pip install -r requirements.txt`
3.  `streamlit run app.py`

## Running with Docker

```bash
docker build -t trello-exporter .
docker run -p 8080:8080 --env-file .env trello-exporter
```

## Deployed Service URL

https://idx-trello-md-v4-09031501-17999627323.europe-west4.run.app

(Deployed manually via `cloudbuild.yaml` — kept as an optional Cloud Run deployment path; not required for occasional local/Codespaces use.)
