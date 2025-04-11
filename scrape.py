from twikit import Client, TooManyRequests, Forbidden
import asyncio
from datetime import datetime
import csv
import io
import random
import time
import os
import glob
import argparse

def get_available_queries():
    """Get list of available query files"""
    query_files = glob.glob('query_*.txt')
    return [os.path.basename(f) for f in query_files]

def select_query_file():
    """Let user select from available query files"""
    query_files = get_available_queries()
    
    if not query_files:
        print("No query files found. Please create query files in the format 'query_*.txt'")
        return None
    
    print("\nAvailable query files:")
    for i, file in enumerate(query_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = int(input("\nSelect a query file (enter number): "))
            if 1 <= choice <= len(query_files):
                return query_files[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(query_files)}")
        except ValueError:
            print("Please enter a valid number")

# Load query content from a selected file
def load_query(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Scrape tweets based on a query')
    parser.add_argument('--query-file', type=str, help='Name of the query file to use')
    args = parser.parse_args()

    # Get query file either from command line or interactive selection
    if args.query_file:
        query_file = args.query_file
        if not os.path.exists(query_file):
            print(f"Error: Query file '{query_file}' not found.")
            return
    else:
        query_file = select_query_file()
        if not query_file:
            return
    
    # Load the selected query
    QUERY = load_query(query_file)
    print(f"\nSelected query from {query_file}:")
    print(f"Query: {QUERY}")
    
    # Initialize client and load cookies
    client = Client(language='en-US')
    try:
        client.load_cookies('cookies.json')
        print("Cookies loaded successfully.")
    except FileNotFoundError:
        print("Error: cookies.json file not found. Please login first using the login script.")
        return
    except Exception as e:
        print(f"Error loading cookies: {str(e)}")
        return

    # Create CSV file with UTF-8 encoding
    output_file = f"tweets_{os.path.splitext(query_file)[0]}.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])
    
    # Search for tweets
    try:
        tweet_count = 0
        tweets = await client.search_tweet(QUERY, product='Top')

        while tweet_count < MINIMUM_TWEETS and tweets:
            for tweet in tweets:
                # Add random delay between processing each tweet (1-3 seconds)
                await asyncio.sleep(random.uniform(1, 3))

                tweet_count += 1

                # Handle text that might contain problematic characters
                try:
                    clean_text = tweet.text
                except:
                    # If text can't be processed, replace with a placeholder
                    clean_text = "[Text contains unsupported characters]"

                tweet_data = [
                    tweet_count,
                    clean_username(tweet.user.name),
                    clean_text,
                    tweet.created_at,
                    tweet.retweet_count,
                    tweet.favorite_count
                ]

                # Write to CSV with UTF-8 encoding
                with open(output_file, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(tweet_data)

                print(f"Added tweet {tweet_count}")

                if tweet_count >= MINIMUM_TWEETS:
                    break

            if tweet_count < MINIMUM_TWEETS:
                print(f"Got {tweet_count} tweets so far. Getting more...")
                # Add longer random delay between batches (3-7 seconds)
                await asyncio.sleep(random.uniform(3, 7))
                tweets = await tweets.next()

        print(f"\nDone! Collected {tweet_count} tweets in total.")
        print(f"Results saved to: {output_file}")

    except TooManyRequests:
        print("Error: Rate limit exceeded. Please wait and try again later.")
    except Forbidden:
        print("Error: Access forbidden. Your cookies might be invalid or expired.")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")

def clean_username(text):
    """Clean username text to avoid encoding issues"""
    if not text:
        return ""
    try:
        # Try to encode and decode as UTF-8
        return text.encode('utf-8', errors='ignore').decode('utf-8')
    except:
        return "[Username contains unsupported characters]"

if __name__ == "__main__":
    MINIMUM_TWEETS = 500
    asyncio.run(main())