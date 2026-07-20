# Fake News Detection

This repository contains a Streamlit frontend and a FastAPI backend for a fake news detection system.

## Setup

1. Install dependencies:
   ```bash
   python -m pip install -r app/requirements.txt
   ```

2. Create a `.env` file with optional environment values:
   ```env
   SHORT_MODEL_NAME=mrm8488/bert-tiny-finetuned-fake-news-detection
   PINECONE_API_KEY=your_api_key_here
   PINECONE_INDEX_HOST=your_index_host_here
   ```

3. Start the API server:
   ```bash
   python main.py
   ```

4. Start the Streamlit frontend:
   ```bash
   python -m streamlit run frontend/app.py
   ```

## Notes

- The frontend posts analysis requests to `http://127.0.0.1:8000/analyze`.
- If Pinecone is not configured, leave the `PINECONE_*` values blank or omit them.
