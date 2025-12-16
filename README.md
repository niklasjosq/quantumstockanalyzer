# Stock News Feeder & AI Analyzer 📈

A powerful, deployment-ready Streamlit application designed for investors to track specific stocks (Quantum Computing focus by default), read real-time news, and leverage Google Gemini AI to analyze SEC filings for potential price impact.

## 🚀 Features

*   **Real-time Stock Dashboard**: Interactive candlestick charts and financial metrics (Price, Market Cap, 52-Week High/Low) powered by `yfinance` and `plotly`.
*   **Rich News Feed**: Aggregated news articles with thumbnails, publishers, and timestamps, cleanly presented in a card layout.
*   **SEC Filings Integration**: Automatic fetching of the latest 8-K and 10-K filings directly from SEC EDGAR RSS feeds.
*   **AI-Powered Analysis**:
    *   Integrates **Google Gemini 1.5 Flash** (via `gemini-flash-latest`) to analyze legal documents.
    *   Provides a **Sentiment Score (0-10)**.
    *   Classifies impact as **Bullish**, **Bearish**, or **Neutral**.
    *   Generates a concise **Executive Summary** and reasoning for the classification.

## 🛠️ Technology Stack

*   **Language**: Python 3.13+
*   **Package Manager**: `uv` (Fastest Python package installer)
*   **Frontend**: Streamlit
*   **Data Sources**:
    *   `yfinance` (Stock data & News)
    *   `feedparser` (SEC EDGAR RSS)
*   **AI/LLM**: `google-generativeai` (Gemini Flash)

## 📦 Installation & Setup

### Prerequisites
1.  **Install `uv`** (if not already installed):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **Get a Google Gemini API Key**: [Get it here](https://aistudio.google.com/app/apikey)

### Local Development

1.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd triple-kepler
    ```

2.  **Run the Application**:
    `uv` handles virtual environment creation and dependency installation automatically.
    ```bash
    uv run streamlit run app.py
    ```

3.  **Access the App**:
    Open [http://localhost:8501](http://localhost:8501) in your browser.

## 📖 Usage Guide

1.  **Sidebar Configuration**:
    *   **API Key**: Paste your Google Gemini API key in the generic password field.
    *   **Stock Selection**: Choose from the curated list (IONQ, RGTI, QUBT, etc.) or type a custom ticker symbol.
    *   **Time Period**: unexpected volatility? Switch the chart view from "1mo" to "1y" or "5y".

2.  **Navigating Tabs**:
    *   **Dashboard**: Overview of current price action.
    *   **Latest News**: Scroll through recent media coverage.
    *   **SEC Filings & Analysis**:
        *   View list of recent regulatory filings.
        *   **Click "Analyze Impact (Gemini)"** on any filing card.
        *   Wait a few seconds for the AI to read and score the filing.

## ☁️ Deployment

This app is ready for deployment on platforms like **Streamlit Cloud**, **Render**, or **Heroku**.

### Streamlit Cloud (Recommended)
1.  Push this repo to GitHub.
2.  Login to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Connect your GitHub account and select this repository.
4.  **Important**: Add your `GOOGLE_API_KEY` (if you want to hardcode it, though the app asks for it in UI for security) or just let users input it.
5.  Click **Deploy**!

## 🤝 Contributing
Feel free to open issues or pull requests.

## 📄 License
MIT License
