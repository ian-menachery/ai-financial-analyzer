import re
from datetime import datetime, timedelta
from typing import List, Dict

class NewsFilter:
    def __init__(self):
        # High-credibility financial news sources (more comprehensive)
        self.tier1_sources = {
            'reuters', 'bloomberg', 'wall street journal', 'financial times', 
            'wsj', 'ft.com', 'cnbc', 'marketwatch', 'seeking alpha',
            'associated press', 'ap news', 'dow jones'
        }
        
        self.tier2_sources = {
            'yahoo finance', 'yahoo entertainment', 'cnn business', 'forbes', 
            'business insider', 'the motley fool', 'benzinga', 'zacks', 
            'barrons', 'investor place', 'thestreet', 'fool.com'
        }
        
        # Enhanced high-impact keywords
        self.high_impact_keywords = {
            'earnings', 'revenue', 'profit', 'loss', 'beat', 'miss', 'guidance',
            'acquisition', 'merger', 'partnership', 'ipo', 'dividend', 'split',
            'ceo', 'cfo', 'layoffs', 'hiring', 'product launch', 'recall',
            'quarterly', 'q1', 'q2', 'q3', 'q4', 'conference call', 'outlook'
        }
        
        # Company-specific keywords (more targeted)
        self.relevance_boosters = {
            'apple inc', 'tim cook', 'iphone', 'ipad', 'mac', 'app store',
            'services revenue', 'hardware sales', 'china sales'
        }
        
        # Noise keywords (expanded)
        self.noise_keywords = {
            'analyst says', 'opinion', 'rumor', 'speculation', 'could', 'might',
            'social media', 'twitter', 'reddit', 'meme', 'sells 145 shares',
            'buys', 'sells', 'shares of', 'price target', 'rating'
    }
    
    def calculate_source_credibility(self, source_name: str) -> float:
        """Rate source credibility from 0.0 to 1.0"""
        source_lower = source_name.lower()
        
        for tier1 in self.tier1_sources:
            if tier1 in source_lower:
                return 1.0
                
        for tier2 in self.tier2_sources:
            if tier2 in source_lower:
                return 0.7
                
        return 0.3  # Unknown sources get low credibility
    
    def calculate_relevance_score(self, article: Dict, ticker: str) -> float:
        """Calculate how relevant an article is to the stock (0.0 to 1.0)"""
        title = article['title'].lower()
        text = f"{title} {article.get('description', '')}".lower()
        ticker_lower = ticker.lower()
        
        relevance_score = 0.0
        
        # Ticker or company name in title gets high relevance
        if ticker_lower in title or 'apple inc' in title:
            relevance_score += 0.5
        elif ticker_lower in text:
            relevance_score += 0.2
        
        # High-impact financial keywords
        impact_words = sum(1 for keyword in self.high_impact_keywords if keyword in text)
        relevance_score += min(impact_words * 0.15, 0.4)
        
        # Company-specific relevance boosters
        company_words = sum(1 for keyword in self.relevance_boosters if keyword in text)
        relevance_score += min(company_words * 0.1, 0.3)
        
        # Heavy penalty for noise (institutional buying/selling news)
        noise_penalty = sum(1 for keyword in self.noise_keywords if keyword in text)
        relevance_score -= min(noise_penalty * 0.2, 0.5)
        
        return max(0.0, min(1.0, relevance_score))
    
    def calculate_time_weight(self, published_at: str) -> float:
        """More recent articles get higher weight"""
        try:
            pub_time = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            now = datetime.now(pub_time.tzinfo)
            hours_ago = (now - pub_time).total_seconds() / 3600
            
            # Weight decays over 72 hours
            return max(0.1, 1.0 - (hours_ago / 72))
        except:
            return 0.5  # Default if parsing fails
    
    def filter_and_rank_articles(self, articles: List[Dict], ticker: str) -> List[Dict]:
        """Filter and rank articles by quality and relevance"""
        scored_articles = []
        
        for article in articles:
            # Calculate scores
            credibility = self.calculate_source_credibility(article['source']['name'])
            relevance = self.calculate_relevance_score(article, ticker)
            time_weight = self.calculate_time_weight(article['publishedAt'])
            
            # Combined quality score
            quality_score = (credibility * 0.4 + relevance * 0.4 + time_weight * 0.2)
            
            # Only keep articles with decent quality
            if quality_score > 0.4:
                scored_articles.append({
                    **article,
                    'credibility_score': credibility,
                    'relevance_score': relevance,
                    'time_weight': time_weight,
                    'quality_score': quality_score
                })
        
        # Sort by quality score, highest first
        scored_articles.sort(key=lambda x: x['quality_score'], reverse=True)
        
        print(f"Filtered {len(articles)} articles down to {len(scored_articles)} high-quality articles")
        
        return scored_articles

# Test the filter
if __name__ == "__main__":
    from news_collector import NewsCollector
    
    collector = NewsCollector()
    filter_system = NewsFilter()
    
    # Get raw articles
    raw_articles = collector.get_stock_news("AAPL", days=5)
    
    if raw_articles:
        # Filter and rank them
        filtered_articles = filter_system.filter_and_rank_articles(raw_articles, "AAPL")
        
        print("\n=== TOP 3 FILTERED ARTICLES ===")
        for i, article in enumerate(filtered_articles[:3]):
            print(f"\n{i+1}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   Credibility: {article['credibility_score']:.2f}")
            print(f"   Relevance: {article['relevance_score']:.2f}")
            print(f"   Quality Score: {article['quality_score']:.2f}")
    else:
        print("No articles found")