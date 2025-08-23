import os
from newsapi import NewsApiClient
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class NewsCollector:
    def __init__(self):
        try:
            api_key = os.getenv('NEWS_API_KEY')
            if not api_key:
                raise Exception("NEWS_API_KEY not found in .env file")
            
            self.newsapi = NewsApiClient(api_key=api_key)
            print("✅ News API initialized")
            
        except Exception as e:
            print(f"❌ Error initializing News API: {e}")
            self.newsapi = None
    
    def get_stock_news(self, ticker, days=7):
        """Get recent news for a stock ticker"""
        if not self.newsapi:
            print("❌ News API not available")
            return []
        
        try:
            # Get company name
            print(f"Looking up company info for {ticker}...")
            stock = yf.Ticker(ticker)
            company_name = stock.info.get('longName', ticker)
            print(f"Found company: {company_name}")
            
            # Calculate date range
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            print(f"Searching news from {from_date}...")
            
            # Search for news
            articles = self.newsapi.get_everything(
                q=f'"{company_name}" OR {ticker}',
                from_param=from_date,
                language='en',
                sort_by='publishedAt',
                page_size=10
            )
            
            print(f"✅ Found {len(articles['articles'])} articles")
            return articles['articles']
            
        except Exception as e:
            print(f"❌ Error fetching news: {e}")
            return []

# Test it
if __name__ == "__main__":
    collector = NewsCollector()
    news = collector.get_stock_news("AAPL")
    
    if news:
        print("\n=== FIRST ARTICLE ===")
        print(f"Title: {news[0]['title']}")
        print(f"Source: {news[0]['source']['name']}")
        print(f"Published: {news[0]['publishedAt']}")
    else:
        print("No news found - check your News API key")