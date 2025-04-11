# Twitter Sentiment Analysis Pipeline

This project provides a complete pipeline for scraping tweets, cleaning them, analyzing sentiment using GPT-4, and visualizing the results.

## Features

- Twitter scraping using twikit
- Tweet cleaning and preprocessing
- Sentiment analysis using GPT-4
- Data analysis and visualization
- Support for multiple query files
- Automated workflow management

## Requirements

- Python 3.8+
- Twitter account (for scraping)
- OpenAI API key (for GPT-4 analysis)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Running the Complete Pipeline

```bash
python main.py
```

### Running Individual Steps

1. Scrape tweets:
```bash
python scrape.py --query-file query_grocery.txt
```

2. Clean tweets:
```bash
python clean_tweets.py
```

3. Analyze sentiment:
```bash
python gpt_summary.py
```

4. Create analysis:
```bash
python create_analysis.py
```

5. Generate visualization:
```bash
python data_viz.py
```

### Command Line Options

- `--start-step`: Start from a specific step (1-5)
- `--skip-requirements`: Skip installing requirements
- `--query-file`: Specify which query file to use

## Project Structure

```
.
├── main.py              # Main workflow controller
├── scrape.py            # Twitter scraping module
├── clean_tweets.py      # Tweet cleaning module
├── gpt_summary.py       # GPT-4 sentiment analysis
├── create_analysis.py   # Data analysis module
├── data_viz.py          # Visualization module
├── query_*.txt          # Query files
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Scraping X.com with Twikit
Credits to this YouTube tutorial: https://youtu.be/6D6fVyFQD5A



