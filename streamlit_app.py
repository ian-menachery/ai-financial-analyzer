import streamlit as st
from advanced_analyzer import AdvancedAnalyzer
import pandas as pd

st.title("🤖 AI Stock Sentiment Analyzer")
st.write("Analyze any stock using AI-powered news sentiment analysis")

# Input section
ticker = st.text_input("Enter Stock Ticker:", value="AAPL").upper()

if st.button("Analyze Stock"):
    with st.spinner(f"Analyzing {ticker}..."):
        analyzer = AdvancedAnalyzer()
        result = analyzer.analyze_stock_sentiment(ticker)
        
        if result:
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Sentiment", f"{result['avg_sentiment']:+.2f}")
            with col2:
                st.metric("Buy Signals", result['buy_signals'])
            with col3:
                st.metric("Sell Signals", result['sell_signals'])
            
            # Show recommendation
            if result['avg_sentiment'] > 0.2:
                st.success("🟢 RECOMMENDATION: BULLISH")
            elif result['avg_sentiment'] < -0.2:
                st.error("🔴 RECOMMENDATION: BEARISH")
            else:
                st.warning("🟡 RECOMMENDATION: NEUTRAL")
            
            # Show detailed analysis
            st.subheader("Article Analysis")
            df = pd.DataFrame(result['detailed_analyses'])
            st.dataframe(df[['sentiment', 'signal', 'title']])
        
        else:
            st.error("Could not analyze - check ticker symbol")