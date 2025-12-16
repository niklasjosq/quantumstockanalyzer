from src.data_fetcher import fetch_news
import json

print("Fetching news for IONQ via DuckDuckGo...")
news = fetch_news("IONQ")
print(json.dumps(news[:3], indent=2))
