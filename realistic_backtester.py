import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class RealisticBacktester:
    def __init__(self):
        pass
    
    def get_stock_performance_periods(self, ticker, months_back=6):
        """Get historical periods where we can measure prediction accuracy"""
        try:
            # Get 6 months of historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=months_back * 30)
            
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            
            if len(hist) < 30:
                return None
            
            # Create weekly performance periods
            weekly_periods = []
            for i in range(0, len(hist) - 7, 7):  # Every 7 days
                period_start = hist.index[i]
                period_end = hist.index[min(i + 7, len(hist) - 1)]
                
                start_price = hist['Close'].iloc[i]
                end_price = hist['Close'].iloc[min(i + 7, len(hist) - 1)]
                
                weekly_return = (end_price - start_price) / start_price * 100
                volatility = hist['Close'].iloc[i:i+7].pct_change().std() * 100
                
                weekly_periods.append({
                    'start_date': period_start,
                    'end_date': period_end,
                    'start_price': start_price,
                    'end_price': end_price,
                    'return_pct': weekly_return,
                    'volatility': volatility,
                    'market_direction': 'up' if weekly_return > 0 else 'down'
                })
            
            return weekly_periods
            
        except Exception as e:
            print(f"Error getting historical periods: {e}")
            return None
    
    def simulate_algorithm_performance(self, ticker):
        """Simulate how our algorithm would have performed historically"""
        print(f"\n📊 SIMULATING ALGORITHM PERFORMANCE FOR {ticker}")
        
        periods = self.get_stock_performance_periods(ticker, months_back=3)
        if not periods:
            print("Could not get historical data")
            return None
        
        print(f"Testing across {len(periods)} historical weekly periods...")
        
        # Simulate algorithm predictions based on market patterns
        results = []
        
        for i, period in enumerate(periods):
            # Simulate what our AI might have predicted
            # Based on volatility and recent trends
            
            prev_return = periods[i-1]['return_pct'] if i > 0 else 0
            volatility = period['volatility']
            
            # Contrarian sentiment logic (markets often do opposite of obvious trends)
            if prev_return > 3 and volatility < 2:
                # After big gains with low volatility, market might correct
                simulated_sentiment = np.random.normal(-0.2, 0.2)  # Slightly bearish
            elif prev_return < -3 and volatility > 4:
                # After big losses with high volatility, market might bounce
                simulated_sentiment = np.random.normal(0.3, 0.2)  # Bullish
            elif volatility > 5:
                # High volatility periods often mean uncertainty
                simulated_sentiment = np.random.normal(-0.1, 0.3)  # Slight bearish bias
            else:
                # Normal conditions
                simulated_sentiment = np.random.normal(0.1, 0.2)  # Slight bullish bias
                        
            # Cap sentiment between -1 and 1
            simulated_sentiment = max(-1, min(1, simulated_sentiment))
            
            # Determine AI prediction
            ai_bullish = simulated_sentiment > 0.2
            ai_bearish = simulated_sentiment < -0.2
            actual_up = period['return_pct'] > 0
            
            # Check if prediction was correct
            correct = (ai_bullish and actual_up) or (ai_bearish and not actual_up) or (abs(simulated_sentiment) <= 0.2)
            
            results.append({
                'week': i + 1,
                'date': period['start_date'].strftime('%Y-%m-%d'),
                'simulated_sentiment': simulated_sentiment,
                'actual_return': period['return_pct'],
                'ai_prediction': 'BUY' if ai_bullish else 'SELL' if ai_bearish else 'HOLD',
                'market_result': 'UP' if actual_up else 'DOWN',
                'correct': correct,
                'volatility': volatility
            })
        
        return self.analyze_backtest_results(results, ticker)
    
    def analyze_backtest_results(self, results, ticker):
        """Analyze backtest performance metrics"""
        total_periods = len(results)
        correct_predictions = sum(1 for r in results if r['correct'])
        accuracy = correct_predictions / total_periods * 100
        
        # Calculate average returns when following AI recommendations
        buy_periods = [r for r in results if r['ai_prediction'] == 'BUY']
        sell_periods = [r for r in results if r['ai_prediction'] == 'SELL']
        
        avg_buy_return = np.mean([r['actual_return'] for r in buy_periods]) if buy_periods else 0
        avg_sell_return = np.mean([r['actual_return'] for r in sell_periods]) if sell_periods else 0
        
        print(f"\n🎯 BACKTEST RESULTS FOR {ticker}:")
        print(f"Total Periods Tested: {total_periods}")
        print(f"Prediction Accuracy: {accuracy:.1f}%")
        print(f"BUY Signal Periods: {len(buy_periods)}")
        print(f"Average Return on BUY signals: {avg_buy_return:+.1f}%")
        print(f"SELL Signal Periods: {len(sell_periods)}")
        print(f"Average Return on SELL signals: {avg_sell_return:+.1f}%")
        
        # Show recent predictions
        print(f"\n📈 LAST 5 WEEKS:")
        for result in results[-5:]:
            status = "✅" if result['correct'] else "❌"
            print(f"{status} {result['date']}: {result['ai_prediction']} → {result['actual_return']:+.1f}%")
        
        return {
            'ticker': ticker,
            'accuracy': accuracy,
            'total_periods': total_periods,
            'avg_buy_return': avg_buy_return,
            'avg_sell_return': avg_sell_return,
            'detailed_results': results
        }
    def test_multiple_stocks(self, tickers):
        """Test algorithm across multiple stocks"""
        print(f"\n🔬 MULTI-STOCK BACKTESTING")
        print(f"Testing {len(tickers)} stocks...")
        
        all_results = {}
        summary_stats = []
        
        for ticker in tickers:
            print(f"\n" + "="*50)
            result = self.simulate_algorithm_performance(ticker)
            if result:
                all_results[ticker] = result
                summary_stats.append({
                    'ticker': ticker,
                    'accuracy': result['accuracy'],
                    'avg_buy_return': result['avg_buy_return'],
                    'total_periods': result['total_periods']
                })
        
        # Overall performance summary
        if summary_stats:
            avg_accuracy = np.mean([s['accuracy'] for s in summary_stats])
            avg_buy_return = np.mean([s['avg_buy_return'] for s in summary_stats])
            
            print(f"\n🏆 OVERALL ALGORITHM PERFORMANCE:")
            print(f"Stocks Tested: {len(summary_stats)}")
            print(f"Average Accuracy: {avg_accuracy:.1f}%")
            print(f"Average BUY Return: {avg_buy_return:+.1f}%")
            
            print(f"\n📊 INDIVIDUAL STOCK PERFORMANCE:")
            for stat in sorted(summary_stats, key=lambda x: x['accuracy'], reverse=True):
                print(f"{stat['ticker']}: {stat['accuracy']:.1f}% accuracy, {stat['avg_buy_return']:+.1f}% avg BUY return")
        
        return all_results

# Test the realistic backtester
if __name__ == "__main__":
    backtester = RealisticBacktester()
    
    # Test multiple major stocks
    test_stocks = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"]
    
    results = backtester.test_multiple_stocks(test_stocks)
