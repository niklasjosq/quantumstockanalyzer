from src.data_fetcher import fetch_stock_info, fetch_sec_filings, fetch_news
import sys

try:
    print("Fetching info for IONQ...")
    info = fetch_stock_info("IONQ")
    print(f"Success. Price: {info.get('currentPrice')}")
except Exception as e:
    print(f"Error fetching info: {e}")

try:
    print("Fetching news for IONQ...")
    news = fetch_news("IONQ")
    print(f"Success. Found {len(news)} articles.")
except Exception as e:
    print(f"Error fetching news: {e}")

try:
    print("Fetching SEC filings for IONQ...")
    filings = fetch_sec_filings("IONQ")
    print(f"Success. Found {len(filings)} filings.")
except Exception as e:
    print(f"Error fetching filings: {e}")
