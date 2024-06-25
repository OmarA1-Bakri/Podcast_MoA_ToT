import logging
from ai_podcast_script_generator import AIPodcastScriptGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        generator = AIPodcastScriptGenerator()
        output = generator.generate_script()
        
        print("Markdown content:")
        print(output["markdown"])
        
        print("\nCSV entry:")
        print(output["csv_entry"])
        
        logger.info("Podcast script generated successfully.")
    except Exception as e:
        logger.error(f"Error generating podcast script: {str(e)}")

if __name__ == "__main__":
    main()
