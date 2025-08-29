from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        # Load API keys from environment
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        
        # Validate API keys
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        if not self.TAVILY_API_KEY:
            print("Warning: TAVILY_API_KEY not found. Search functionality will be disabled.")
        
        # Allowed model names
        self.ALLOWED_MODEL_NAMES = [
            "llama3-70b-8192",
            "llama-3.3-70b-versatile"
        ]

# Create settings instance
settings = Settings()