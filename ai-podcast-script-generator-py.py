import logging
from typing import Dict
from rss_processor import RSSProcessor
from mixture_of_agents import MixtureOfAgents
from output_generator import OutputGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIPodcastScriptGenerator:
    def __init__(self):
        self.rss_processor = RSSProcessor()
        self.moa = MixtureOfAgents()
        self.output_generator = OutputGenerator()

    def generate_script(self) -> Dict[str, str]:
        try:
            # Step 1: Fetch and process RSS feed
            articles = self.rss_processor.fetch_top_stories()

            # Step 2: Generate script using Mixture of Agents
            script_content = self.moa.process(articles)

            # Step 3: Generate output files
            md_content = self.output_generator.generate_markdown(script_content)
            csv_entry = self.output_generator.update_csv(script_content)

            return {
                "markdown": md_content,
                "csv_entry": csv_entry
            }
        except Exception as e:
            logger.error(f"Error generating podcast script: {str(e)}")
            raise
