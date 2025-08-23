import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()

class AdvancedAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print("✅ Advanced Analyzer ready")
    
    def analyze_article(self, article):
        """Get numerical sentiment score and trading signal"""
        try:
            article_text = f"{article['title']}. {article.get('description', '')}"
            
            prompt = f"""
            You are a financial analyst. Analyze this news for stock impact.
            
            News: {article_text}
            
            Respond with exactly this format:
            SENTIMENT: [number from -1.0 to 1.0]
            SIGNAL: [BUY/SELL/HOLD]
            REASON: [one sentence explanation]
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.1
            )
            
            text = response.choices[0].message.content.strip()
            
            # Parse the response
            sentiment_match = re.search(r'SENTIMENT:\s*([-+]?\d*\.?\d+)', text)
            signal_match = re.search(r'SIGNAL:\s*(\w+)', text)
            reason_match = re.search(r'REASON:\s*(.+)', text)
            
            if sentiment_match and signal_match:
                return {
                    'sentiment': float(sentiment_match.group(1)),
                    'signal': signal_match.group(1).upper(),
                    'reason': reason_match.group(1) if reason_match else "No reason provided",
                    'title': article['title']
                }
            else:
                print(f"❌ Could not parse response: {text}")
                return None
                
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return None
    
    def analyze_stock_sentiment(self, ticker):
        """Analyze overall sentiment for a stock"""
        from news_collector import NewsCollector
        
        collector = NewsCollector()
        news = collector.get_stock_news(ticker, days=5)
        
        if not news:
            return None
        
        analyses = []
        print(f"\nAnalyzing {len(news[:7])} articles for {ticker}...")
        
        for article in news[:7]:  # Analyze 7 articles
            analysis = self.analyze_article(article)
            if analysis:
                analyses.append(analysis)
                print(f"  {analysis['sentiment']:+.2f} | {analysis['signal']} | {analysis['title'][:50]}...")
        
        if not analyses:
            return None
        
        # Calculate overall metrics
        avg_sentiment = sum(a['sentiment'] for a in analyses) / len(analyses)
        buy_signals = sum(1 for a in analyses if a['signal'] == 'BUY')
        sell_signals = sum(1 for a in analyses if a['signal'] == 'SELL')
        
        return {
            'ticker': ticker,
            'avg_sentiment': avg_sentiment,
            'total_articles': len(analyses),
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'detailed_analyses': analyses
        }

# Test it
if __name__ == "__main__":
    analyzer = AdvancedAnalyzer()
    result = analyzer.analyze_stock_sentiment("AAPL")
    
    if result:
        print(f"\n🎯 FINAL ANALYSIS FOR {result['ticker']}:")
        print(f"Average Sentiment: {result['avg_sentiment']:+.2f}")
        print(f"Buy Signals: {result['buy_signals']}")
        print(f"Sell Signals: {result['sell_signals']}")
        
        if result['avg_sentiment'] > 0.2:
            print("🟢 RECOMMENDATION: BULLISH")
        elif result['avg_sentiment'] < -0.2:
            print("🔴 RECOMMENDATION: BEARISH")
        else:
            print("🟡 RECOMMENDATION: NEUTRAL")