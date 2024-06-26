"""
moa_framework.py

This module implements the Mix of Agents (MoA) framework for the AI News Podcast Generation System.
It coordinates the different types of agents and manages the overall workflow of generating a podcast script.
"""

from typing import List, Dict
from rss_feed_parser import RSSFeedParser
from specific_agent_classes import ChiefEditorAgent, ManagerAgent, WorkerAgent
from config import Config
import concurrent.futures
import logging

logger = logging.getLogger(__name__)

class MoAFramework:
    """
    Mix of Agents (MoA) Framework for generating AI news podcast scripts.

    This class coordinates the different types of agents (Chief Editor, Managers, and Workers)
    and manages the overall workflow of generating a podcast script from RSS feed input.

    Attributes:
        rss_parser (RSSFeedParser): Parser for retrieving top stories from an RSS feed.
        chief_editor (ChiefEditorAgent): The Chief Editor agent for final script review.
        manager_agents (Dict[str, ManagerAgent]): Dictionary of Manager agents for different roles.
        worker_agents (Dict[str, List[WorkerAgent]]): Dictionary of lists of Worker agents for each role.
    """

    def __init__(self, rss_feed_url: str, tavily_api_key: str):
        """
        Initialize the MoAFramework.

        Args:
            rss_feed_url (str): URL of the RSS feed to parse for news stories.
            tavily_api_key (str): API key for Tavily internet search service.
        """
        self.rss_parser = RSSFeedParser(rss_feed_url)
        self.chief_editor = ChiefEditorAgent("Chief Editor", tavily_api_key)
        self.manager_agents = {
            "news_editor": ManagerAgent("News Editor", "News Editor", tavily_api_key),
            "journalist": ManagerAgent("Journalist", "Journalist", tavily_api_key),
            "script_writer": ManagerAgent("Script Writer", "Script Writer", tavily_api_key)
        }
        self.worker_agents = {
            "news_editor": [WorkerAgent(f"news_editor_Worker_{i}", tavily_api_key) for i in range(1, Config.MAX_WORKERS + 1)],
            "journalist": [WorkerAgent(f"journalist_Worker_{i}", tavily_api_key) for i in range(1, Config.MAX_WORKERS + 1)],
            "script_writer": [WorkerAgent(f"script_writer_Worker_{i}", tavily_api_key) for i in range(1, Config.MAX_WORKERS + 1)]
        }

    def process_worker_layer(self, agent_type: str, input: str) -> str:
        """
        Process input through a layer of worker agents.

        Args:
            agent_type (str): The type of worker agents to use.
            input (str): The input to process.

        Returns:
            str: The processed output from the worker layer.

        Raises:
            ValueError: If the agent_type is not recognized.
        """
        if agent_type not in self.worker_agents:
            raise ValueError(f"Unknown worker agent type: {agent_type}")
        if agent_type not in self.manager_agents:
            raise ValueError(f"Unknown manager agent type: {agent_type}")

        worker_outputs = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
            future_to_worker = {executor.submit(worker.process, input): worker for worker in self.worker_agents[agent_type]}
            for future in concurrent.futures.as_completed(future_to_worker):
                worker = future_to_worker[future]
                try:
                    result = future.result()
                    worker_outputs.append(result)
                except Exception as e:
                    logger.error(f"Worker {worker.name} generated an exception: {str(e)}")
        
        return self.manager_agents[agent_type].process("\n\n".join(worker_outputs))

    def generate_podcast_script(self) -> str:
        """
        Generate a complete podcast script using the Mix of Agents framework.

        This method orchestrates the entire process of generating a podcast script:
        1. Fetches top stories from the RSS feed
        2. Processes the stories through the News Editor layer
        3. Passes the result through the Journalist layer
        4. Creates a script using the Script Writer layer
        5. Finalizes the script with the Chief Editor

        Returns:
            str: The final podcast script.

        Raises:
            Exception: If there's an error at any stage of the generation process.
        """
        try:
            # Get top stories from RSS feed
            top_stories = self.rss_parser.get_top_stories(num_stories=Config.NUM_STORIES, days=Config.DAYS_LOOKBACK)

            # Process through News Editor layer
            news_editor_input = "\n\n".join([f"Title: {story['title']}\nSummary: {story['summary']}" for story in top_stories])
            news_editor_output = self.process_worker_layer("news_editor", news_editor_input)

            # Process through Journalist layer
            journalist_output = self.process_worker_layer("journalist", news_editor_output)

            # Process through Script Writer layer
            script_writer_output = self.process_worker_layer("script_writer", journalist_output)

            # Final processing by Chief Editor
            final_script = self.chief_editor.process([news_editor_output, journalist_output, script_writer_output])

            return final_script
        except Exception as e:
            logger.error(f"Error in generate_podcast_script: {str(e)}")
            raise
