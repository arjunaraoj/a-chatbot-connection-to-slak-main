# 🤖 A Chatbot Connection to Slack (LangChain + OpenAI)

This project enables a Slack chatbot that can query structured (CSV, JSON) and unstructured (PDF) sales data using LangChain, FAISS, and OpenAI.

## Features
- Slack bot with `/ask` command and app mention support
- Answers business questions from your data
- LangChain + FAISS for smart document search
- Gradio interface for local dev testing

## Setup
1. Clone the repo
2. Copy `.env.example` to `.env` and fill credentials
3. Run `pip install -r requirements.txt`
4. Start bot with `python app/app.py`
