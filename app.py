
import streamlit as st
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import re

# Load environment variables from .env file
load_dotenv()

# Trello API credentials
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")

def sanitize_markdown(text):
    # Remove headings
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove bold and italics
    text = re.sub(r'\*\*|\*', '', text)
    # Remove strikethrough
    text = re.sub(r'~~', '', text)
    # Remove blockquotes
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    # Remove horizontal rules
    text = re.sub(r'^-{3,}\s*$', '', text, flags=re.MULTILINE)
    # Remove list markers
    text = re.sub(r'^\s*([-*+]|\d+\.)\s+', '', text, flags=re.MULTILINE)
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

# Function to get Trello workspaces (organizations)
def get_trello_workspaces():
    url = f"https://api.trello.com/1/members/me/organizations?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch Trello workspaces: {e}. Please check your API key and token.")
        return []

# Function to get Trello boards for a workspace
def get_trello_boards(workspace_id):
    url = f"https://api.trello.com/1/organizations/{workspace_id}/boards?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}&filter=open"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch Trello boards: {e}")
        return []

# Function to get detailed Trello board data
def get_trello_board_data(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}&lists=open&cards=open&card_fields=all&card_attachments=true&checklists=all"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch detailed board data: {e}")
        return None

# Function to get comments for a card
def get_card_comments(card_id):
    url = f"https://api.trello.com/1/cards/{card_id}/actions?filter=commentCard&key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch comments for card {card_id}: {e}")
        return []

# Function to generate detailed markdown from board data
def generate_markdown(board_data, progress_placeholder):
    export_date = datetime.now().strftime("%Y-%m-%d")
    
    open_lists = [l for l in board_data['lists'] if not l['closed']]

    markdown = f"# {board_data['name']}\n\n---\n"
    markdown += f"- Number of cards: {len(board_data['cards'])}\n"
    markdown += f"- Number of lists: {len(open_lists)}\n"

    for trello_list in open_lists:
        list_card_count = len([card for card in board_data['cards'] if card['idList'] == trello_list['id']])
        markdown += f"  - {trello_list['name']} ({list_card_count})\n"

    markdown += f"- Export date: {export_date}\n\n---\n\n"

    checklists_map = {c['id']: c for c in board_data.get('checklists', [])}

    for i, trello_list in enumerate(open_lists):
        list_cards = [card for card in board_data['cards'] if card['idList'] == trello_list['id']]
        markdown += f"## {trello_list['name']}\n\n"
        markdown += f"- Number of cards: {len(list_cards)}\n\n"

        for j, card in enumerate(list_cards):
            progress_placeholder.text(f"Fetching card {j+1}/{len(list_cards)} in list '{trello_list['name']}'")
            markdown += f"### {card['name']}\n\n"
            
            if card['labels']:
                markdown += f"- Labels: { ', '.join([l['name'] for l in card['labels']]) }\n"
            if card['desc']:
                description = sanitize_markdown(card['desc']).replace('\n', '\n  ')
                markdown += f"- Description: {description}\n"
            if card['start']:
                markdown += f"- Start date: {datetime.fromisoformat(card['start'][:-1]).strftime('%Y-%m-%d')}\n"
            if card['due']:
                markdown += f"- Due date: {datetime.fromisoformat(card['due'][:-1]).strftime('%Y-%m-%d')}\n"

            if card.get('attachments'):
                for attachment in card['attachments']:
                    mime_type = attachment.get('mimeType')
                    is_image = (mime_type and mime_type.startswith('image')) or (attachment.get('previews'))
                    if is_image:
                        markdown += f"- Image: {attachment['url']}\n"

            if card.get('idChecklists'):
                for checklist_id in card['idChecklists']:
                    checklist = checklists_map.get(checklist_id)
                    if checklist:
                        markdown += f"- Checklist {checklist['name']}\n"
                        for item in checklist.get('checkItems', []):
                            checked = "[X]" if item['state'] == 'complete' else "[ ]"
                            due_date = f" (Due date: {datetime.fromisoformat(item['due'][:-1]).strftime('%Y-%m-%d')})" if item.get('due') else ""
                            markdown += f"  - {checked} {item['name']}{due_date}\n"
            
            card_comments = sorted(get_card_comments(card['id']), key=lambda c: c['date'])
            for comment in card_comments:
                comment_date = datetime.fromisoformat(comment['date'][:-1]).strftime('%Y-%m-%d %H:%M:%S')
                comment_text = sanitize_markdown(comment['data']['text'])
                markdown += f"- {comment_date}: {comment_text}\n"

            creation_date = datetime.fromtimestamp(int(card['id'][0:8], 16)).strftime('%Y-%m-%d')
            last_activity_date = datetime.fromisoformat(card['dateLastActivity'][:-1]).strftime('%Y-%m-%d')
            markdown += f"- Created: {creation_date}\n"
            markdown += f"- Updated: {last_activity_date}\n"
            markdown += f"- ID: {card['idShort']}\n"
            markdown += f"- URL: {card['shortUrl']}\n\n"
    progress_placeholder.empty()
    return markdown

# Streamlit UI
st.title("Trello to Markdown Exporter")

if not TRELLO_API_KEY or not TRELLO_API_TOKEN:
    st.warning("Trello API key and token not found. Please create a .env file with TRELLO_API_KEY and TRELLO_API_TOKEN.")
else:
    workspaces = get_trello_workspaces()
    if workspaces:
        workspace_names = [w['displayName'] for w in workspaces]
        selected_workspace_name = st.selectbox("Select a Trello Workspace", workspace_names)

        if selected_workspace_name:
            selected_workspace_id = [w['id'] for w in workspaces if w['displayName'] == selected_workspace_name][0]
            boards = get_trello_boards(selected_workspace_id)

            if boards:
                board_names = [b['name'] for b in boards]
                selected_board_name = st.selectbox("Select a Trello Board", board_names)

                if selected_board_name:
                    selected_board_id = [b['id'] for b in boards if b['name'] == selected_board_name][0]

                    col1, col2 = st.columns(2)

                    with col1:
                        progress_placeholder = st.empty()
                        if st.button("Generate Markdown"):
                            board_data = get_trello_board_data(selected_board_id)
                            if board_data:
                                st.session_state.markdown_content = generate_markdown(board_data, progress_placeholder)
                                st.session_state.board_name = board_data['name']
                                st.session_state.export_date = datetime.now().strftime("%Y-%m-%d")

                    if 'markdown_content' in st.session_state:
                        with col2:
                            safe_board_name = re.sub(r'[\\/:*?"<>|]', '', st.session_state.board_name)
                            st.download_button(
                                label="Download Markdown File",
                                data=st.session_state.markdown_content,
                                file_name=f"{st.session_state.export_date} Trello {safe_board_name}.md",
                                mime="text/markdown"
                            )

    if 'markdown_content' in st.session_state:
        st.subheader("Generated Markdown Preview")
        st.markdown(st.session_state.markdown_content)
