import feedparser
import pandas as pd
import requests
import yfinance as yf

try:
    from ddgs import DDGS  # Preferred package name.
except ImportError:
    DDGS = None

def fetch_stock_history(ticker_symbol, period="1y"):
    """
    Fetches historical stock data using yfinance.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.history(period=period)
    except Exception as e:
        print(f"Error fetching stock history for {ticker_symbol}: {e}")
        return pd.DataFrame()

def fetch_stock_info(ticker_symbol):
    """
    Fetches basic stock info.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.info
    except Exception as e:
        print(f"Error fetching stock info for {ticker_symbol}: {e}")
        return {}


def _fetch_news_from_yfinance(ticker_symbol):
    """
    Fallback source for news if DDGS is unavailable or returns no data.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        raw_news = ticker.news or []
    except Exception as e:
        print(f"Error fetching fallback Yahoo Finance news: {e}")
        return []

    cleaned_news = []
    for item in raw_news:
        content = item.get("content", {})
        title = content.get("title")
        link_obj = content.get("clickThroughUrl") or content.get("canonicalUrl") or {}
        link = link_obj.get("url")

        if not title or not link:
            continue

        provider = content.get("provider") or {}
        thumbnail = content.get("thumbnail") or {}

        cleaned_news.append(
            {
                "title": title,
                "link": link,
                "publisher": provider.get("displayName", "Yahoo Finance"),
                "publishTime": content.get("pubDate", "Recent"),
                "thumbnail": thumbnail.get("originalUrl"),
                "summary": content.get("summary", ""),
            }
        )

    return cleaned_news

def fetch_news(ticker_symbol):
    """
    Fetches latest news for the stock using DuckDuckGo News Search.
    This provides a Google News-like experience with reliable links.
    """
    try:
        if DDGS is None:
            return _fetch_news_from_yfinance(ticker_symbol)

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
            
        if cleaned_news:
            return cleaned_news
        
    except Exception as e:
        print(f"Error fetching news from DDG: {e}")

    return _fetch_news_from_yfinance(ticker_symbol)

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
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
    except requests.RequestException as e:
        print(f"Error fetching SEC filings for {ticker_symbol}: {e}")
        return []
    
    if response.status_code != 200:
        return []
        
    feed = feedparser.parse(response.content)
    
    filings = []
    for entry in feed.entries:
        filings.append({
            'title': entry.get("title", "Untitled Filing"),
            'link': entry.get("link", ""),
            'summary': entry.get("summary", "No summary available."),
            'updated': entry.get("updated", "N/A"),
            'category': entry.get("category", "N/A")
        })
    
    return filings
