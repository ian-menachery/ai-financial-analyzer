# AI-Powered Financial News Analyzer
A system that analyzes real-time financial news using GPT-4 to generate trading signals and risk assessments for equity investments.
Features
AI Sentiment Analysis

Processes real-time financial news using OpenAI GPT-4
Generates numerical sentiment scores (-1.0 to +1.0)
Provides BUY/SELL/HOLD recommendations with confidence levels

Market Integration

Fetches live stock price data and historical trends
Compares AI predictions with actual market movements
Identifies agreement/disagreement between sentiment and price action

Risk Assessment

Calculates confidence scores for each analysis
Monitors news volume and article relevance
Generates risk warnings for volatile or low-conviction signals
Provides conviction levels (HIGH/MEDIUM/LOW)

Interactive Web Interface

Streamlit dashboard for stock analysis
Real-time analysis of publicly traded securities
Visual metrics and detailed article breakdowns

Technology Stack

AI/ML: OpenAI GPT-4 API, Natural Language Processing
Data: NewsAPI, Yahoo Finance API integration
Backend: Python, pandas for data processing
Frontend: Streamlit web framework
APIs: RESTful API integration with error handling

Sample Analysis Output
ENHANCED ANALYSIS FOR AAPL:
AI Sentiment: +0.16
Market Change: -0.7%
Confidence: 0.69
Conviction: MEDIUM
News Volume: 0.7/1.0
AI and Market DISAGREE
Setup Instructions

Clone the repository:
bashgit clone https://github.com/ian-menachery/ai-financial-analyzer.git
cd ai-financial-analyzer

Install dependencies:
bashpip install -r requirements.txt

Set up API keys:
Create a .env file with:
OPENAI_API_KEY=your-openai-key-here
NEWS_API_KEY=your-newsapi-key-here

Run the application:
bashstreamlit run streamlit_app.py


Usage

Enter any stock ticker (AAPL, TSLA, NVDA, etc.)
View AI sentiment analysis of recent news
Compare with actual market performance
Review risk warnings and confidence metrics
Get actionable trading recommendations

Project Highlights

Real-time data processing from multiple financial news sources
Advanced natural language processing using large language models
Risk management capabilities with confidence scoring and volatility detection
Production-ready web interface with responsive design
Quantitative validation through comparison of predictions with market performance
