import csv
from datetime import datetime
import glob
import os

def create_analysis_file():
    # Find the most recent sentiment labels file
    sentiment_files = glob.glob('03_sentiment_labels.csv')
    if not sentiment_files:
        print("No sentiment labels file found. Please run the sentiment analysis step first.")
        return 1
    
    input_file = sentiment_files[0]  # There should only be one
    output_file = '04_data_analysis.csv'
    
    print(f"Processing {input_file}...")

    # Read data from both files
    tweets_data = {}
    sentiment_data = {}

    # Read tweets
    tweet_files = glob.glob('01_tweets_*.csv')
    if not tweet_files:
        print("No tweet files found. Please run the scraping step first.")
        return 1
    
    tweets_file = max(tweet_files, key=os.path.getctime)
    with open(tweets_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tweets_data[row['Tweet_count']] = {
                'date': row['Created At'],
                'text': row['Text']
            }

    # Read sentiment scores
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Print the header to debug
        print("Columns in sentiment file:", reader.fieldnames)
        for row in reader:
            sentiment_data[row['id']] = {
                'score': row['score'],  # Changed from stance_score to score
                'explanation': row['explanation']
            }

    # Create the combined analysis file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'score', 'date'])  # Write header
        
        # Combine data and write to new file
        for tweet_id in tweets_data:
            if tweet_id in sentiment_data:
                writer.writerow([
                    tweet_id,
                    sentiment_data[tweet_id]['score'],
                    tweets_data[tweet_id]['date']
                ])

    print(f"Analysis complete. Results saved to {output_file}")
    return 0

if __name__ == "__main__":
    exit(create_analysis_file()) 