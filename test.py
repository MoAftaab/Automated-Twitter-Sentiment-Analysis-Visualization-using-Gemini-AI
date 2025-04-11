from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio  # Add this import for async support

MINIMUM_TWEETS = 10
QUERY = '(finance OR wealth OR investment) min_retweets:2500 since:2025-04-07 -filter:replies'

# Create an async main function
async def main():
    #* login credentials
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    #* authenticate to X.com
    client = Client(language='en-US')
    client.load_cookies('cookies.json')

    #* get tweets - use await here
    tweets = await client.search_tweet(QUERY, product='Top')

    # Now we can iterate through the tweets
    for tweet in tweets:
        print(vars(tweet))
        break

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())