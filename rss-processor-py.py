import feedparser
from typing import List, Dict
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RSSProcessor:
    def __init__(self, feed_url: str = "https://example.com/ai_stories.rss"):
        self.feed_url = feed_url

    def fetch_top_stories(self, num_stories: int = 10, days: int = 7) -> List[Dict[str, str]]:
        try:
            feed = feedparser.parse(self.feed_url)
            
            # Sort entries by published date and rating (you might need to adjust this based on your RSS feed structure)
            sorted_entries = sorted(feed.entries, key=lambda entry: (entry.published_parsed, float(entry.get('rating', 0))), reverse=True)
            
            # Filter for the last 7 days
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_entries = [
                entry for entry in sorted_entries 
                if datetime(*entry.published_parsed[:6]) > cutoff_date
            ]
            
            # Take the top 10
            top_entries = recent_entries[:num_stories]
            
            return [
                {
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.summary,
                    "published": datetime(*entry.published_parsed[:6]).isoformat(),
                    "rating": entry.get('rating', 'N/A')
                } 
                for entry in top_entries
            ]
        except Exception as e:
            logger.error(f"Error fetching RSS feed: {str(e)}")
            raise
