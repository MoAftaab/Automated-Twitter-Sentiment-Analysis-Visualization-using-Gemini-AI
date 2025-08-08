# Configuration file for dataset paths and settings

# Dataset Configuration
DATASET_CONFIG = {
    # Default dataset (comes with the project)
    "default": "01_tweets_query_grocery.csv",
    
    # Add your own datasets here
    # Example:
    # "my_dataset": "path/to/my_tweets.csv",
    # "large_dataset": "data/large_twitter_dataset.csv",
}

# Analysis Settings
ANALYSIS_CONFIG = {
    "rate_limit_delay": 4,  # seconds between API calls
    "batch_size": 20,       # tweets to process in one batch
    "max_retries": 3,       # retry failed API calls
}

# File Paths
FILE_PATHS = {
    "raw_tweets": "01_tweets_*.csv",
    "cleaned_tweets": "02_cleaned_tweets.csv", 
    "sentiment_labels": "03_sentiment_labels.csv",
    "analysis_results": "04_data_analysis.csv",
    "visualization": "05_sentiment_analysis.png",
    "raw_json": "gpt_analysis.json"
}

def get_dataset_path(dataset_name="default"):
    """Get the path for a specific dataset"""
    return DATASET_CONFIG.get(dataset_name, DATASET_CONFIG["default"])

def list_available_datasets():
    """List all available datasets"""
    return list(DATASET_CONFIG.keys())