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

from duckduckgo_search import DDGS

def fetch_news(ticker_symbol):
    """
    Fetches latest news for the stock using DuckDuckGo News Search.
    This provides a Google News-like experience with reliable links.
    """
    try:
        # Search for "Ticker Stock News"
        query = f"{ticker_symbol} stock news"
        
        with DDGS() as ddgs:
            # get 10 news results
            results = list(ddgs.news(query, max_results=10))
            
        cleaned_news = []
        for item in results:
            # DDGS returns: {'title':..., 'body':..., 'date':..., 'image':..., 'source':..., 'url':...}
            title = item.get('title')
            link = item.get('url')
            
            if not title or not link:
                continue
                
            cleaned_news.append({
                'title': title,
                'link': link,
                'publisher': item.get('source', 'Unknown Source'),
                'publishTime': item.get('date', 'Recent'),
                'thumbnail': item.get('image'),
                'summary': item.get('body', '') 
            })
            
        return cleaned_news
        
    except Exception as e:
        print(f"Error fetching news from DDG: {e}")
        return []

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
