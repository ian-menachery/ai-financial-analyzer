import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from news_filter import NewsFilter

load_dotenv()

class AdvancedAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print("✅ Advanced Analyzer ready")
    
    def analyze_article(self, article):
        """Get enhanced sentiment analysis with confidence scoring"""
        try:
            article_text = f"{article['title']}. {article.get('description', '')}"
            
            prompt = f"""
            You are a financial analyst. Analyze this news for stock impact.
            
            News: {article_text}
            
            Consider:
            - How specific and factual is this news?
            - How directly does it relate to company performance?
            - How significant is the impact mentioned?
            
            Respond with exactly this format:
            SENTIMENT: [number from -1.0 to 1.0]
            CONFIDENCE: [number from 0.0 to 1.0]
            SIGNAL: [BUY/SELL/HOLD]
            REASON: [one sentence explanation]
            RELEVANCE: [HIGH/MEDIUM/LOW]
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=120,
                temperature=0.1
            )
            
            text = response.choices[0].message.content.strip()
            
            # Parse the enhanced response
            sentiment_match = re.search(r'SENTIMENT:\s*([-+]?\d*\.?\d+)', text)
            confidence_match = re.search(r'CONFIDENCE:\s*([-+]?\d*\.?\d+)', text)
            signal_match = re.search(r'SIGNAL:\s*(\w+)', text)
            reason_match = re.search(r'REASON:\s*(.+)', text)
            relevance_match = re.search(r'RELEVANCE:\s*(\w+)', text)
            
            if sentiment_match and confidence_match and signal_match:
                return {
                    'sentiment': float(sentiment_match.group(1)),
                    'confidence': float(confidence_match.group(1)),
                    'signal': signal_match.group(1).upper(),
                    'reason': reason_match.group(1) if reason_match else "No reason provided",
                    'relevance': relevance_match.group(1) if relevance_match else "MEDIUM",
                    'title': article['title']
                }
            else:
                print(f"❌ Could not parse response: {text}")
                return None
                
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return None
    
    def analyze_stock_sentiment(self, ticker):
        """Analyze overall sentiment for a stock using filtered, high-quality news"""
        from news_collector import NewsCollector
        
        collector = NewsCollector()
        filter_system = NewsFilter()
        
        # Get raw news
        raw_news = collector.get_stock_news(ticker, days=5)
        
        if not raw_news:
            return None
        
        # Filter and rank articles by quality
        filtered_news = filter_system.filter_and_rank_articles(raw_news, ticker)
        
        if not filtered_news:
            print("No high-quality articles found after filtering")
            return None
        
        analyses = []
        print(f"\nAnalyzing {len(filtered_news)} high-quality articles for {ticker}...")
        
        # Analyze only the filtered, high-quality articles
        for article in filtered_news:
            analysis = self.analyze_article(article)
            if analysis:
                # Weight the analysis by article quality
                analysis['quality_weight'] = article['quality_score']
                analysis['source_credibility'] = article['credibility_score']
                analyses.append(analysis)
                print(f"  {analysis['sentiment']:+.2f} | {analysis['signal']} | Quality: {article['quality_score']:.2f} | {analysis['title'][:50]}...")
        
        if not analyses:
            return None
        
        # Calculate quality-weighted metrics
        total_weight = sum(a['quality_weight'] for a in analyses)
        weighted_sentiment = sum(a['sentiment'] * a['quality_weight'] for a in analyses) / total_weight
        
        buy_signals = sum(1 for a in analyses if a['signal'] == 'BUY')
        sell_signals = sum(1 for a in analyses if a['signal'] == 'SELL')
        
        return {
            'ticker': ticker,
            'avg_sentiment': weighted_sentiment,
            'total_articles': len(analyses),
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'detailed_analyses': analyses,
            'raw_articles_count': len(raw_news),
            'filtered_articles_count': len(filtered_news)
    }
    def get_stock_price_data(self, ticker):
        """Get recent stock price data"""
        try:
            import yfinance as yf
            
            stock = yf.Ticker(ticker)
            
            # Get 30 days of data
            hist = stock.history(period="1mo")
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            week_ago_price = hist['Close'].iloc[-7] if len(hist) >= 7 else hist['Close'].iloc[0]
            
            # Calculate price change
            price_change = current_price - week_ago_price
            price_change_percent = (price_change / week_ago_price) * 100
            
            print(f"📈 {ticker} Price Data:")
            print(f"  Current: ${current_price:.2f}")
            print(f"  Week ago: ${week_ago_price:.2f}")
            print(f"  Change: {price_change_percent:+.2f}%")
            
            return {
                'current_price': current_price,
                'week_ago_price': week_ago_price,
                'price_change_percent': price_change_percent,
                'direction': 'up' if price_change > 0 else 'down' if price_change < 0 else 'flat'
            }
        
        except Exception as e:
            print(f"❌ Error getting price data: {e}")
            return None
        

    def calculate_risk_metrics(self, analyses, price_data):
        """Calculate risk warnings and confidence metrics"""
        if not analyses or not price_data:
            return {}
        
        # News volume analysis
        high_relevance = sum(1 for a in analyses if a.get('relevance') == 'HIGH')
        total_articles = len(analyses)
        news_volume_score = min(total_articles / 10.0, 1.0)  # Normalize to 0-1
        
        # Confidence analysis
        avg_confidence = sum(a.get('confidence', 0.5) for a in analyses) / len(analyses)
        
        # Disagreement analysis
        sentiment_direction = "bullish" if sum(a['sentiment'] for a in analyses) > 0 else "bearish"
        market_direction = "bullish" if price_data['direction'] == 'up' else "bearish"
        agreement = sentiment_direction == market_direction
        
        # Risk warnings
        risk_warnings = []
        
        if avg_confidence < 0.6:
            risk_warnings.append("Low confidence in news analysis")
        
        if total_articles < 3:
            risk_warnings.append("Limited news coverage - low conviction")
        
        if abs(price_data['price_change_percent']) > 5:
            risk_warnings.append("High volatility detected")
        
        if not agreement:
            risk_warnings.append("AI sentiment conflicts with market movement")
        
        return {
            'news_volume_score': news_volume_score,
            'avg_confidence': avg_confidence,
            'high_relevance_articles': high_relevance,
            'agreement_with_market': agreement,
            'risk_warnings': risk_warnings,
            'conviction_level': 'HIGH' if avg_confidence > 0.7 and total_articles >= 5 else 
                            'MEDIUM' if avg_confidence > 0.5 and total_articles >= 3 else 'LOW'
        }
# Test it



if __name__ == "__main__":
    analyzer = AdvancedAnalyzer()
    
    # Test all features together
    ticker = "AAPL"
    sentiment_result = analyzer.analyze_stock_sentiment(ticker)
    price_data = analyzer.get_stock_price_data(ticker)
    
    if sentiment_result and price_data:
        # Calculate risk metrics
        risk_metrics = analyzer.calculate_risk_metrics(
            sentiment_result['detailed_analyses'], 
            price_data
        )
        
        print(f"\n🎯 ENHANCED ANALYSIS FOR {ticker}:")
        print(f"AI Sentiment: {sentiment_result['avg_sentiment']:+.2f}")
        print(f"Market Change: {price_data['price_change_percent']:+.1f}%")
        print(f"Confidence: {risk_metrics['avg_confidence']:.2f}")
        print(f"Conviction: {risk_metrics['conviction_level']}")
        print(f"News Volume: {risk_metrics['news_volume_score']:.1f}/1.0")
        
        if risk_metrics['agreement_with_market']:
            print("✅ AI and Market AGREE")
        else:
            print("⚠️  AI and Market DISAGREE")
        
        # Show risk warnings
        if risk_metrics['risk_warnings']:
            print(f"\n⚠️  RISK WARNINGS:")
            for warning in risk_metrics['risk_warnings']:
                print(f"  • {warning}")
        else:
            print("\n✅ No major risk warnings detected")
    
    else:
        print("❌ Analysis failed")