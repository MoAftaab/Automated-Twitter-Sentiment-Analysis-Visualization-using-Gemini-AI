# Twitter Sentiment Analysis Pipeline

This project provides a complete pipeline for scraping tweets, cleaning them, analyzing sentiment using GPT-4, and visualizing the results.

## ⚠️ Security Notice

- Never commit your API keys or sensitive credentials to the repository
- Use `.env` file for storing sensitive information
- The repository includes `.gitignore` to prevent accidental commits of sensitive files
- Copy `.env.example` to `.env` and fill in your own values

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
```bash
# Copy the example environment file
cp .env.example .env
# Edit .env with your actual values
# NEVER commit .env to the repository
```

5. Set up Twitter authentication:
```bash
# Create a config.ini file with your Twitter credentials:
# [X]
# username = your_twitter_username
# email = your_twitter_email
# password = your_twitter_password

# Run the authentication script
python 00_setup_auth.py
```
This will generate a `cookies.json` file that the scraper will use for authentication.

## Usage

### Running the Complete Pipeline

```bash
python main.py
```

### Running Individual Steps

1. Scrape tweets:
```bash
python 01_scrape_tweets.py --query-file query_grocery.txt
```

2. Clean tweets:
```bash
python 02_clean_tweets.py
```

3. Analyze sentiment:
```bash
python 03_analyze_sentiment.py
```

4. Create analysis:
```bash
python 04_create_analysis.py
```

5. Generate visualization:
```bash
python 05_generate_visualization.py
```

### Command Line Options

- `--start-step x`: Start from a specific step (1-5)
- `--skip-requirements`: Skip installing requirements
- `--query-file`: Specify which query file to use

## Project Structure

```
.
├── main.py                      # Main workflow controller
├── 00_setup_auth.py             # Twitter authentication
├── 01_scrape_tweets.py          # Twitter scraping module
├── 02_clean_tweets.py           # Tweet cleaning module
├── 03_analyze_sentiment.py      # GPT-4 sentiment analysis
├── 04_create_analysis.py        # Data analysis module
├── 05_generate_visualization.py # Visualization module
├── query_*.txt                  # Query files
├── requirements.txt             # Project dependencies
├── .env.example                 # Example environment variables
└── README.md                    # Project documentation
```

## Output Files

The pipeline generates the following files in sequence:
1. `01_tweets_*.csv` - Raw scraped tweets
2. `02_cleaned_tweets.csv` - Cleaned and processed tweets
3. `03_sentiment_labels.csv` - GPT-4 sentiment analysis results
4. `04_data_analysis.csv` - Combined analysis data
5. `05_sentiment_analysis.png` - Visualization of results

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



