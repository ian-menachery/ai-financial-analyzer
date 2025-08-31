import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from advanced_analyzer import AdvancedAnalyzer
import time

class Backtester:
    def __init__(self):
        self.analyzer = AdvancedAnalyzer()
        
    def get_historical_prices(self, ticker, start_date, end_date):
        """Get historical stock prices"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            return hist
        except Exception as e:
            print(f"Error getting historical data: {e}")
            return None
    
    def backtest_single_date(self, ticker, analysis_date):
        """Test AI prediction for a single date"""
        print(f"\n📅 Backtesting {ticker} for {analysis_date.strftime('%Y-%m-%d')}")
        
        # Simulate analyzing news on that date
        # (In real backtesting, we'd use historical news APIs)
        try:
            # For now, we'll use current news analysis as a proxy
            # In production, you'd use historical news data
            result = self.analyzer.analyze_stock_sentiment(ticker)
            
            if not result:
                return None
            
            # Get stock price performance after the analysis
            next_week = analysis_date + timedelta(days=7)
            prices = self.get_historical_prices(ticker, analysis_date, next_week)
            
            if prices is None or len(prices) < 2:
                return None
            
            start_price = prices['Close'].iloc[0]
            end_price = prices['Close'].iloc[-1]
            actual_return = (end_price - start_price) / start_price * 100
            
            # Determine if AI prediction was correct
            ai_bullish = result['avg_sentiment'] > 0.2
            ai_bearish = result['avg_sentiment'] < -0.2
            market_up = actual_return > 0
            
            correct_prediction = (ai_bullish and market_up) or (ai_bearish and not market_up)
            
            return {
                'date': analysis_date,
                'ticker': ticker,
                'ai_sentiment': result['avg_sentiment'],
                'actual_return': actual_return,
                'ai_bullish': ai_bullish,
                'ai_bearish': ai_bearish,
                'market_up': market_up,
                'correct_prediction': correct_prediction,
                'confidence': result.get('avg_confidence', 0.5),
                'articles_analyzed': result['filtered_articles_count']
            }
            
        except Exception as e:
            print(f"Error in backtest: {e}")
            return None

# Quick test
if __name__ == "__main__":
    backtester = Backtester()
    
    # Test with a recent date
    test_date = datetime.now() - timedelta(days=14)
    result = backtester.backtest_single_date("AAPL", test_date)
    
    if result:
        print(f"\n🎯 BACKTEST RESULT:")
        print(f"AI Sentiment: {result['ai_sentiment']:+.2f}")
        print(f"Actual 7-day Return: {result['actual_return']:+.1f}%")
        print(f"Prediction Correct: {'✅' if result['correct_prediction'] else '❌'}")
    else:
        print("Backtest failed")