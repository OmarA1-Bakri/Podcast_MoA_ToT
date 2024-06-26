"""
rss_feed_parser.py

This module provides functionality to parse RSS feeds and extract top stories
for the AI News Podcast Generation System.
"""

import feedparser
from typing import List, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RSSFeedError(Exception):
    """Custom exception class for RSS Feed-related errors."""
    pass

class RSSFeedParser:
    """
    A class to parse RSS feeds and extract top stories.

    This class provides methods to fetch and process RSS feeds, filtering stories
    based on recency and popularity.

    Attributes:
        feed_url (str): The URL of the RSS feed to parse.
    """

    def __init__(self, feed_url: str):
        """
        Initialize the RSSFeedParser.

        Args:
            feed_url (str): The URL of the RSS feed to parse.
        """
        self.feed_url = feed_url

    def get_top_stories(self, num_stories: int = 10, days: int = 7) -> List[Dict]:
        """
        Fetch and process top stories from the RSS feed.

        This method retrieves stories from the RSS feed, filters them based on
        recency, sorts them by popularity (currently using the number of comments
        as a proxy for popularity), and returns the top stories.

        Args:
            num_stories (int, optional): The number of top stories to return. Defaults to 10.
            days (int, optional): The number of days to look back for stories. Defaults to 7.

        Returns:
            List[Dict]: A list of dictionaries containing the top stories. Each dictionary
                        contains 'title', 'link', 'summary', and 'published' keys.

        Raises:
            RSSFeedError: If there's an error parsing the RSS feed or processing the stories.
        """
        try:
            # Parse the RSS feed
            feed = feedparser.parse(self.feed_url)
            
            if feed.bozo:
                raise RSSFeedError(f"Error parsing RSS feed: {feed.bozo_exception}")
            
            # Calculate the cutoff date for recent stories
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Filter stories from the last 'days' days
            recent_stories = [
                entry for entry in feed.entries
                if datetime(*entry.published_parsed[:6]) > cutoff_date
            ]
            
            # Sort stories by popularity (using number of comments as a proxy)
            # Note: This sorting method may need to be adjusted based on the actual RSS feed structure
            sorted_stories = sorted(recent_stories, key=lambda x: len(x.get('comments', [])), reverse=True)
            
            # Select the top N stories
            top_stories = sorted_stories[:num_stories]
            
            # Format the stories for output
            return [
                {
                    'title': story.title,
                    'link': story.link,
                    'summary': story.summary,
                    'published': story.published
                }
                for story in top_stories
            ]
        except RSSFeedError as e:
            logger.error(f"RSS Feed Error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in RSS Feed Parser: {str(e)}")
            raise RSSFeedError(f"Unexpected error in RSS Feed Parser: {str(e)}")

