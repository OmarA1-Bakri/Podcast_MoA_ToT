"""
rss_feed_parser.py

This module provides functionality to parse RSS feeds and extract top stories
for the AI News Podcast Generation System.
"""

import requests
from bs4 import BeautifulSoup
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

    def __init__(self, url):
        """
        Initialize the RSSFeedParser.

        Args:
            url (str): The URL of the website to scrape for news.
        """
        self.url = url

    def get_top_stories(self, num_stories=10, days=7):
        """
        Fetch and process top stories from the website.

        This method retrieves stories from the website, filters them based on
        recency, and returns the top stories.

        Args:
            num_stories (int, optional): The number of top stories to return. Defaults to 10.
            days (int, optional): The number of days to look back for stories. Defaults to 7.

        Returns:
            List[Dict]: A list of dictionaries containing the top stories. Each dictionary
                        contains 'title', 'link', 'summary', and 'published' keys.

        Raises:
            RSSFeedError: If there's an error fetching or parsing the news content.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = soup.find_all('div', class_='news-item')

            stories = []
            for item in news_items[:num_stories]:
                title = item.find('h3', class_='news-title').text.strip()
                summary = item.find('p', class_='news-summary').text.strip()
                link = item.find('a', class_='news-link')['href']
                date_str = item.find('span', class_='news-date').text.strip()
                
                # Parse the date (adjust the format as needed)
                pub_date = datetime.strptime(date_str, "%B %d, %Y")
                
                if pub_date > (datetime.now() - timedelta(days=days)):
                    stories.append({
                        'title': title,
                        'summary': summary,
                        'link': link,
                        'published': pub_date
                    })

            return stories

        except requests.RequestException as e:
            logger.error(f"Error fetching news: {str(e)}")
            raise RSSFeedError(f"Error fetching news: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing news content: {str(e)}")
            raise RSSFeedError(f"Error parsing news content: {str(e)}")
