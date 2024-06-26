import os
import csv
from datetime import datetime
from moa_framework import MoAFramework
from config import Config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ensure_output_directory():
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)

def save_markdown(content: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{Config.OUTPUT_DIR}/podcast_script_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(content)
    return filename

def update_csv(md_filename: str):
    csv_filename = f"{Config.OUTPUT_DIR}/podcast_scripts.csv"
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, "a", newline="") as csvfile:
        fieldnames = ["Timestamp", "Markdown_Filename"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Markdown_Filename": os.path.basename(md_filename)
        })

def main():
    try:
        Config.validate()
        ensure_output_directory()
        
        moa = MoAFramework(Config.RSS_FEED_URL, Config.TAVILY_API_KEY)
        
        logger.info("Generating podcast script...")
        podcast_script = moa.generate_podcast_script()
        
        logger.info("Saving output files...")
        md_filename = save_markdown(podcast_script)
        update_csv(md_filename)
        
        logger.info(f"Podcast script generated and saved as {md_filename}")
        logger.info(f"CSV file updated with new entry")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

