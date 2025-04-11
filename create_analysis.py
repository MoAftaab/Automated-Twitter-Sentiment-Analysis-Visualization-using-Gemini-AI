import csv
from datetime import datetime

def create_analysis_file():
    # Read data from both files
    tweets_data = {}
    with open('tweets.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert tweet count to id (assuming tweet_count starts at 1)
            tweet_id = int(row['Tweet_count'])
            # Parse the date and format it - updated format to match 'Fri Mar 14 01:40:07 +0000 2025'
            date = datetime.strptime(row['Created At'], '%a %b %d %H:%M:%S +0000 %Y').strftime('%Y-%m-%d')
            tweets_data[tweet_id] = date

    # Read sentiment scores
    sentiment_data = {}
    with open('senti_labels.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tweet_id = int(row['id'])
            score = row['score']
            sentiment_data[tweet_id] = score

    # Create the combined analysis file
    with open('data_analysis.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'score', 'date'])  # Write header
        
        # Write data for all 88 records
        for tweet_id in range(1, 89):
            date = tweets_data.get(tweet_id, '')
            score = sentiment_data.get(tweet_id, '')
            writer.writerow([tweet_id, score, date])

    print("Successfully created data_analysis.csv with 88 records")

if __name__ == "__main__":
    create_analysis_file() 