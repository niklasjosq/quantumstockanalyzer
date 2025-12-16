# Stock News Feeder 📈

A Streamlit application to track specific stocks, read news, and analyze SEC filings with Google Gemini Flash.

## Features
- **Real-time Stock Data**: Interactive charts and key metrics via `yfinance`.
- **Latest News**: Aggregated news feed for each stock.
- **SEC Filings**: Automatic fetching of recent 8-K/10-K filings from SEC EDGAR.
- **AI Analysis**: meaningful summaries and impact analysis of filings using Google Gemini 1.5 Flash.

## Setup

1.  **Install `uv`** (if not installed):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Run the App**:
    ```bash
    uv run streamlit run app.py
    ```

3.  **Using the App**:
    - Open the link (usually `http://localhost:8501`).
    - Enter your **Google Gemini API Key** in the sidebar.
    - Select a stock (e.g., IONQ, RGTI) to view dashboard and filings.
    - Click "Analyze Impact" on any SEC filing to get an AI-powered summary.

## Tech Stack
- **Frontend**: Streamlit
- **Data**: yfinance, feedparser (SEC RSS)
- **AI**: Google Gemini (via `google-generativeai`)
