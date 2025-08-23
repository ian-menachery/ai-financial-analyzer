from news_collector import NewsCollector
from llm_analyzer import LLMAnalyzer

def analyze_stock(ticker):
    """Get news for a stock and analyze each article"""
    print(f"\n=== ANALYZING {ticker} ===")
    
    # Get news
    collector = NewsCollector()
    news = collector.get_stock_news(ticker, days=3)
    
    if not news:
        print("No news found")
        return
    
    # Analyze each article
    analyzer = LLMAnalyzer()
    results = []
    
    for i, article in enumerate(news[:5]):  # Analyze first 5 articles
        print(f"\nArticle {i+1}: {article['title'][:60]}...")
        sentiment = analyzer.analyze_article(article)
        
        results.append({
            'title': article['title'],
            'sentiment': sentiment,
            'source': article['source']['name'],
            'published': article['publishedAt']
        })
    
    # Show summary
    print(f"\n=== SUMMARY FOR {ticker} ===")
    positive = sum(1 for r in results if r['sentiment'] == 'positive')
    negative = sum(1 for r in results if r['sentiment'] == 'negative')
    neutral = sum(1 for r in results if r['sentiment'] == 'neutral')
    
    print(f"Positive articles: {positive}")
    print(f"Negative articles: {negative}")
    print(f"Neutral articles: {neutral}")
    
    if positive > negative:
        print("🟢 Overall sentiment: BULLISH")
    elif negative > positive:
        print("🔴 Overall sentiment: BEARISH")
    else:
        print("🟡 Overall sentiment: NEUTRAL")

if __name__ == "__main__":
    # Test with Apple
    analyze_stock("AAPL")