#!/bin/sh
source .venv/bin/activate
streamlit run app.py --server.headless=true --server.address=0.0.0.0 --server.port ${PORT:-8501} --server.enableCORS=false --server.enableXsrfProtection=false
