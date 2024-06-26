# AI News Podcast Script Generator

This project implements an AI-powered system for generating podcast scripts based on the latest AI news. It uses a Mix of Agents (MoA) framework combined with a Tree of Thought (ToT) algorithm to process news from RSS feeds and create engaging podcast content.

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

## Features

- Fetches top AI news stories from RSS feeds
- Utilizes a Mix of Agents (MoA) framework for diverse perspective generation
- Implements Tree of Thought (ToT) algorithm for structured problem-solving
- Parallel processing of worker agents for improved performance
- Generates podcast scripts in Markdown format
- Maintains a CSV log of generated scripts

## Architecture

The system is composed of several key components:

1. **RSS Feed Parser**: Fetches and processes top AI news stories from specified RSS feeds.

2. **Mix of Agents (MoA) Framework**: Coordinates different types of agents to process the news and generate the script.

3. **Agent Types**:
   - Chief Editor Agent (Claude 3.5 Sonnet)
   - Manager Agents (Claude 3.5 Sonnet):
     - News Editor Manager
     - Journalist Manager
     - Script Writer Manager
   - Worker Agents (Claude 3.0 Haiku):
     - News Editor Workers
     - Journalist Workers
     - Script Writer Workers

4. **Tree of Thought (ToT) Algorithm**: Implemented within each agent for structured problem-solving and content generation.

5. **Parallel Processing**: Worker agents operate in parallel to improve performance.

6. **Output Generation**: Creates podcast scripts in Markdown format and maintains a CSV log of generated scripts.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-news-podcast-generator.git
   cd ai-news-podcast-generator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the project root directory with the following content:
   ```
   RSS_FEED_URL=https://example.com/ai_news_rss_feed
   TAVILY_API_KEY=your_tavily_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Usage

To generate a podcast script:

1. Ensure your virtual environment is activated.

2. Run the main script:
   ```
   python main.py
   ```

3. The generated podcast script will be saved in the `output` directory as a Markdown file, and an entry will be added to the `podcast_scripts.csv` file.

## Configuration

You can customize the behavior of the script generator by modifying the `config.py` file. This file contains settings for:

- RSS feed URL
- Number of stories to process
- Days to look back for news
- Agent models
- Tree of Thought parameters
- Output directory
- Parallel processing settings

## Testing

To run the unit tests:

```
python -m unittest discover tests
```

## Contributing

Contributions to this project are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

