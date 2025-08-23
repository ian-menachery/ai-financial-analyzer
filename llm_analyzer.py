import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print("✅ LLM Analyzer ready")
    
    def analyze_article(self, article):
        """Simple analysis that just gets sentiment"""
        try:
            article_text = f"{article['title']}. {article.get('description', '')}"
            
            prompt = f"""
            Is this financial news positive, negative, or neutral for the stock?
            
            News: {article_text}
            
            Just respond with one word: positive, negative, or neutral
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            
            sentiment = response.choices[0].message.content.strip().lower()
            print(f"✅ Article sentiment: {sentiment}")
            return sentiment
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return "error"

# Simple test
if __name__ == "__main__":
    analyzer = LLMAnalyzer()
    
    # Test with a fake article
    test_article = {
        'title': 'Apple Reports Record iPhone Sales',
        'description': 'Apple exceeded expectations with strong quarterly results'
    }
    
    result = analyzer.analyze_article(test_article)
    print(f"Final result: {result}")