import pandas as pd
import re
import emoji
import sys
import glob
import os

def clean_text(text):
    """Clean tweet text by removing URLs, mentions, emojis, and special characters"""
    if pd.isna(text):
        return ""
        
    # Convert to string if not already
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags but keep the text
    text = re.sub(r'#', '', text)
    
    # Remove emojis
    text = emoji.replace_emoji(text, '')
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def main():
    # Find the most recent tweets file
    tweet_files = glob.glob('01_tweets_*.csv')
    if not tweet_files:
        print("No tweet files found. Please run the scraping step first.")
        return 1
    
    input_file = max(tweet_files, key=os.path.getctime)
    output_file = '02_cleaned_tweets.csv'
    
    print(f"Processing {input_file}...")
    
    print("Loading tweets.csv...")
    try:
        # Read CSV with UTF-8 encoding
        df = pd.read_csv(input_file, encoding='utf-8')
    except UnicodeDecodeError:
        # If UTF-8 fails, try with different encoding
        print("UTF-8 encoding failed, trying with ISO-8859-1...")
        df = pd.read_csv(input_file, encoding='ISO-8859-1')
    except FileNotFoundError:
        print("Error: tweets.csv not found!")
        return 1
    
    print(f"Processing {len(df)} tweets...")
    
    # Clean the tweet text
    df['Text'] = df['Text'].apply(clean_text)
    
    # Remove empty tweets
    df = df.dropna(subset=['Text'])
    df = df[df['Text'].str.strip() != '']
    
    print(f"Saving {len(df)} cleaned tweets...")
    
    try:
        # Save to cleaned_tweets.csv with UTF-8 encoding
        df.to_csv(output_file, index=False, encoding='utf-8')
        print("Successfully saved cleaned_tweets.csv")
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        # Set console to UTF-8 mode
        if sys.platform == 'win32':
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass
    
    exit(main()) 