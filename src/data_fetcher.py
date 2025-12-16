import yfinance as yf
import feedparser
import pandas as pd
from datetime import datetime

def fetch_stock_history(ticker_symbol, period="1y"):
    """
    Fetches historical stock data using yfinance.
    """
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)
    return hist

def fetch_stock_info(ticker_symbol):
    """
    Fetches basic stock info.
    """
    ticker = yf.Ticker(ticker_symbol)
    return ticker.info

def fetch_news(ticker_symbol):
    """
    Fetches latest news for the stock using yfinance (which scrapes Yahoo Finance).
    """
    ticker = yf.Ticker(ticker_symbol)
    news = ticker.news
    
    # yfinance news structure can be nested under 'content' key
    cleaned_news = []
    for item in news:
        content = item.get('content', item) # Fallback if not nested
        cleaned_news.append({
            'title': content.get('title'),
            'link': content.get('clickThroughUrl', {}).get('url'),
            'publisher': content.get('provider', {}).get('displayName'),
            'publishTime': content.get('pubDate'), # This is ISO format string
            'thumbnail': content.get('thumbnail', {}).get('resolutions', [{}])[0].get('url') if content.get('thumbnail') else None
        })
        
    return cleaned_news

def fetch_sec_filings(ticker_symbol):
    """
    Fetches recent SEC filings using the SEC EDGAR Atom feed.
    Note: Using the ticker directly in the CIK parameter often works for widely traded stocks.
    """
    # RSS Feed URL for SEC EDGAR
    # type=8-K covers major events. We can leave type blank for all.
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker_symbol}&type=&dateb=&owner=exclude&start=0&count=20&output=atom"
    
    # User-Agent is required by SEC
    headers = {'User-Agent': 'Mozilla/5.0 (StreamlitApp; +http://streamlit.io) python-requests/1.0'}
    
    # feedparser allows passing a dictionary as request_headers? No, it usually manages it or needs a helper.
    # Actually feedparser downloads content itself. But SEC is strict about User-Agent.
    # We might need to fetch with requests first.
    
    import requests
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []
        
    feed = feedparser.parse(response.content)
    
    filings = []
    for entry in feed.entries:
        filings.append({
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary,
            'updated': entry.updated,
            'category': entry.category if hasattr(entry, 'category') else 'N/A'
        })
    
    return filings
