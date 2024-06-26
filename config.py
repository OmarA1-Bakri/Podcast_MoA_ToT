import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # RSS Feed settings
    RSS_FEED_URL = "https://www.futuretools.io/news"
    NUM_STORIES = 10
    DAYS_LOOKBACK = 7

    # Agent settings
    CHIEF_EDITOR_MODEL = "claude-3-5-sonnet-20240620"
    MANAGER_MODEL = "claude-3-5-sonnet-20240620"
    WORKER_MODEL = "claude-3-haiku-20240307"
    TOT_MAX_DEPTH = 2
    TOT_BRANCHING_FACTOR = 2

    # API keys
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    # Output settings
    OUTPUT_DIR = "output"

    # Parallel processing settings
    MAX_WORKERS = 3

    @classmethod
    def validate(cls):
        required_env_vars = ["RSS_FEED_URL", "TAVILY_API_KEY", "ANTHROPIC_API_KEY"]
        missing_vars = [var for var in required_env_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
