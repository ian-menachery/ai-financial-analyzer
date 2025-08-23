import os
from dotenv import load_dotenv
from openai import OpenAI

# Load your API keys
load_dotenv()

def test_openai_connection():
    try:
        # Check if API key exists
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ Error: OPENAI_API_KEY not found in .env file")
            print("Make sure your .env file has: OPENAI_API_KEY=sk-your-key-here")
            return False
        
        if not api_key.startswith('sk-'):
            print("❌ Error: OpenAI API key should start with 'sk-'")
            return False
        
        print("Testing OpenAI connection...")
        
        # Test OpenAI connection
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Hello from your AI financial analyzer!'"}],
            max_tokens=50
        )
        
        print("✅ OpenAI Response:", response.choices[0].message.content)
        print("✅ Setup complete! Ready to build your AI analyzer.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if "quota" in str(e).lower():
            print("💡 Solution: Add $5 to your OpenAI account at platform.openai.com")
        elif "authentication" in str(e).lower():
            print("💡 Solution: Check your API key in the .env file")
        return False

if __name__ == "__main__":
    test_openai_connection()