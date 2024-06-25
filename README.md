# AI Podcast Script Generator

This project implements an AI-powered system to generate podcast scripts based on the top 10 highest-rated AI stories from an RSS feed. It uses a Mix of Agents (MoA) framework and Tree of Thought (ToT) algorithmic iteration to create engaging and informative scripts.

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Dependencies](#dependencies)
7. [Contributing](#contributing)
8. [License](#license)

## Features

- Fetches and processes the top 10 highest-rated AI stories from an RSS feed
- Employs a three-layer agent structure for script generation:
  - Chief Editor Agent
  - Manager Agents (News Editor, Journalist, Script Agent)
  - Worker Agents
- Utilizes Tree of Thought processing for iterative refinement
- Generates output in Markdown format
- Updates a CSV file with script summaries
- Integrates with Tavily API for internet search capabilities

## Architecture

The system follows this high-level process:

1. RSS Feed Processing
2. News Editor Agent processing
3. Worker Agents (3x) with Tree of Thought processing
4. Journalist Agent processing
5. Worker Agents (3x) with Tree of Thought processing
6. Script Agent processing
7. Worker Agents (3x) with Tree of Thought processing
8. Chief Editor Agent final processing
9. Generate Markdown output
10. Update CSV file

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-podcast-generator.git
   cd ai-podcast-generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your API keys:
     ```
     ANTHROPIC_API_KEY=your_anthropic_api_key
     TAVILY_API_KEY=your_tavily_api_key
     ```

## Usage

To generate a podcast script:

```python
from ai_podcast_script_generator import AIPodcastScriptGenerator

generator = AIPodcastScriptGenerator()
output = generator.generate_script()

print("Markdown content:", output["markdown"])
print("CSV entry:", output["csv_entry"])
```

## Configuration

You can configure the following parameters in the `AIPodcastScriptGenerator` class:

- RSS feed URL
- Number of top stories to fetch
- Time range for stories (default is 7 days)
- Tree of Thought depth and branching factor
- Output CSV filename

## Dependencies

- Python 3.7+
- feedparser
- anthropic
- tavily-python
- python-dotenv

See `requirements.txt` for a full list of dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
