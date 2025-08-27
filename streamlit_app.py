import streamlit as st
from advanced_analyzer import AdvancedAnalyzer
import pandas as pd

st.title("🤖 Enhanced AI Stock Analyzer")
st.write("AI sentiment + market data + risk assessment")

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input("Enter Stock Ticker:", value="AAPL").upper()
with col2:
    st.write("")
    st.write("")
    analyze_button = st.button("Analyze Stock", type="primary")

if analyze_button:
    with st.spinner(f"Analyzing {ticker}..."):
        analyzer = AdvancedAnalyzer()
        
        # Get all data
        sentiment_result = analyzer.analyze_stock_sentiment(ticker)
        price_data = analyzer.get_stock_price_data(ticker)
        
        if sentiment_result and price_data:
            risk_metrics = analyzer.calculate_risk_metrics(
                sentiment_result['detailed_analyses'], 
                price_data
            )
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("AI Sentiment", f"{sentiment_result['avg_sentiment']:+.2f}")
            with col2:
                st.metric("Stock Price", f"${price_data['current_price']:.2f}", 
                         f"{price_data['price_change_percent']:+.1f}%")
            with col3:
                st.metric("Confidence", f"{risk_metrics['avg_confidence']:.2f}")
            with col4:
                st.metric("Conviction", risk_metrics['conviction_level'])
            
            # Agreement/Disagreement Analysis
            if risk_metrics['agreement_with_market']:
                st.success("✅ AI and Market AGREE - Higher Confidence Signal")
            else:
                st.warning("⚠️ AI and Market DISAGREE - Proceed with Caution")
            
            # Risk Warnings
            if risk_metrics['risk_warnings']:
                st.error("🚨 Risk Warnings:")
                for warning in risk_metrics['risk_warnings']:
                    st.write(f"• {warning}")
            else:
                st.success("✅ No major risk factors detected")
            
            # News Volume Indicator
            news_volume = risk_metrics['news_volume_score']
            if news_volume > 0.8:
                st.info(f"📰 High news volume ({sentiment_result['total_articles']} articles) - Strong signal")
            elif news_volume < 0.3:
                st.warning(f"📰 Low news volume ({sentiment_result['total_articles']} articles) - Weak signal")
            
            # Final Recommendation
            st.subheader("🎯 Final Recommendation")
            
            if (sentiment_result['avg_sentiment'] > 0.3 and 
                risk_metrics['avg_confidence'] > 0.6 and 
                len(risk_metrics['risk_warnings']) <= 1):
                st.success("🟢 STRONG BUY - High confidence bullish signal")
            elif (sentiment_result['avg_sentiment'] < -0.3 and 
                  risk_metrics['avg_confidence'] > 0.6):
                st.error("🔴 STRONG SELL - High confidence bearish signal")
            elif abs(sentiment_result['avg_sentiment']) < 0.2:
                st.warning("🟡 HOLD - Neutral sentiment")
            else:
                st.info("🔵 WEAK SIGNAL - Low confidence or high risk")
            
            # Detailed breakdown
            with st.expander("📊 Detailed Article Analysis"):
                df = pd.DataFrame(sentiment_result['detailed_analyses'])
                st.dataframe(df[['sentiment', 'confidence', 'signal', 'relevance', 'title']])
        
        else:
            st.error("❌ Could not analyze - check ticker symbol")

# Add sidebar with tips
st.sidebar.title("How to Use")
st.sidebar.write("""
**Signal Strength:**
- 🟢 STRONG BUY: High confidence + bullish sentiment
- 🔴 STRONG SELL: High confidence + bearish sentiment  
- 🟡 HOLD: Neutral or conflicted signals
- 🔵 WEAK: Low confidence or high risk

**Risk Factors:**
- Agreement between AI and market
- News volume and relevance
- Confidence in AI analysis
""")