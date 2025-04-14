import os
import csv
import json
from openai import OpenAI
from dotenv import load_dotenv
import emoji
import sys
import glob

# Load environment variables from the .env file
load_dotenv()

# Ensure your API key is set as an environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Set console encoding to UTF-8 on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def remove_emojis(text):
    """Remove emojis from text"""
    return emoji.replace_emoji(text, replace='')

def get_tweet_texts(csv_filename):
    """
    Reads the CSV file and returns a list of tuples containing (id, tweet_text)
    """
    tweets = []
    with open(csv_filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Get headers
        print(f"CSV Headers: {headers}")  # Print headers for debugging
        
        # Determine column indices based on headers
        id_col = 0  # Tweet_count is first column
        text_col = 2  # Text is third column
        
        for row in csv_reader:
            if row and len(row) > max(id_col, text_col):  # Ensure row has enough columns
                tweets.append((row[id_col], row[text_col]))  # (id, tweet_text)
    
    print(f"Loaded {len(tweets)} tweets from CSV")
    return tweets

def get_insights_from_gpt(tweet_id, tweet_text):
    """
    Sends a single tweet to GPT-4 (gpt-4o) to analyze and generate insights.
    """
    print(f"\nAnalyzing tweet {tweet_id}:")
    # Remove emojis and clean text for display
    clean_text = remove_emojis(tweet_text)
    print(f"Tweet text: {clean_text[:100]}...")  # Print first 100 chars of cleaned tweet
    
    # Prepare prompt (input) with the tweet data
    prompt = f"""
You are a sentiment analysis assistant. Your task is to evaluate a tweet about food prices and classify it on a satisfaction scale where:
    
1 = Very unsatisfied (strong anger, frustration, or outrage about food prices)
2 = Unsatisfied (disappointment or complaints about food prices)
3 = Neutral (observational, balanced or mixed feelings about food prices)
4 = Satisfied (approval or mild praise, noting price improvements)
5 = Very satisfied (enthusiastic approval or strong praise regarding affordability)

Analyze the following tweet and return: - 1. the stance score along - 2. a brief explanation for your classification

Your output should be in the following JSON format:

{{
  "id": "{tweet_id}",
  "stance_score": 3,
  "explanation": "brief rationale"
}}

Here is the tweet: {tweet_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a senior social media sentiment analyst. Your task is to evaluate tweets about food prices and classify it on a satisfaction scale for news reporting."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content
        print(f"GPT Response: {result}")
        return result
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return None

def clean_json_response(response):
    """
    Cleans the GPT response by removing markdown formatting
    """
    if not response:
        return None
        
    # Remove markdown code block formatting if present
    if response.startswith('```json'):
        response = response[7:]  # Remove ```json
    if response.startswith('```'):
        response = response[3:]  # Remove ```
    if response.endswith('```'):
        response = response[:-3]  # Remove ```
    
    # Remove any leading/trailing whitespace
    response = response.strip()
    
    return response

def save_to_json(analysis_result, json_filename='gpt_analysis.json'):
    """
    Saves the GPT-4 analysis results to a JSON file
    """
    if not analysis_result:
        print("No analysis result to save")
        return False
        
    try:
        # Clean the response before parsing
        cleaned_result = clean_json_response(analysis_result)
        if not cleaned_result:
            print("Failed to clean JSON response")
            return False
            
        # Parse the JSON result
        result = json.loads(cleaned_result)
        print(f"Parsed JSON result: {result}")
        
        # Read existing JSON file if it exists
        if os.path.exists(json_filename):
            with open(json_filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print(f"Existing JSON data length: {len(data)}")
        else:
            data = []
            print("No existing JSON file found, creating new one")
        
        # Add new result
        data.append(result)
        
        # Write back to JSON file
        with open(json_filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
            
        print(f"Successfully saved analysis for tweet {result['id']} to {json_filename}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {cleaned_result}")
        print(f"JSONDecodeError details: {str(e)}")
        return False
    except Exception as e:
        print(f"Error saving to {json_filename}: {str(e)}")
        print(f"Analysis result that caused error: {analysis_result}")
        return False

def convert_json_to_csv(json_filename='gpt_analysis.json', csv_filename='03_sentiment_labels.csv'):
    """
    Converts the JSON analysis results to CSV format
    """
    try:
        # Read JSON file
        with open(json_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if not data:
            print(f"No data found in {json_filename}")
            return False
            
        # Write to CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'score', 'explanation'])  # Write header
            
            for item in data:
                writer.writerow([
                    item.get('id', ''),
                    item.get('stance_score', ''),
                    item.get('explanation', '')
                ])
        
        print(f"Successfully converted {json_filename} to {csv_filename}")
        return True
        
    except FileNotFoundError:
        print(f"JSON file {json_filename} not found")
        return False
    except Exception as e:
        print(f"Error converting JSON to CSV: {str(e)}")
        return False

def main():
    # Find the most recent cleaned tweets file
    cleaned_files = glob.glob('02_cleaned_tweets.csv')
    if not cleaned_files:
        print("No cleaned tweets file found. Please run the cleaning step first.")
        return 1
    
    input_file = cleaned_files[0]  # There should only be one
    output_file = '03_sentiment_labels.csv'
    
    print(f"Processing {input_file}...")
    
    # Initialize empty JSON file (overwrite if exists)
    with open('gpt_analysis.json', 'w', encoding='utf-8') as file:
        json.dump([], file)
    
    # Clear the output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'score', 'explanation'])  # Write header
    
    # Read tweets from the CSV file
    tweets = get_tweet_texts(input_file)
    print(f"\nTotal tweets to process: {len(tweets)}")
    
    # Process tweets one by one
    success_count = 0
    for i, (tweet_id, tweet_text) in enumerate(tweets, 1):
        print(f"\nProcessing tweet {i}/{len(tweets)} (ID: {tweet_id})")
        analysis = get_insights_from_gpt(tweet_id, tweet_text)
        if analysis and save_to_json(analysis):
            success_count += 1
            print(f"Successfully processed tweet {tweet_id}")
        else:
            print(f"Failed to process tweet {tweet_id}")
    
    print(f"\nSummary: Successfully analyzed {success_count} out of {len(tweets)} tweets")
    
    # Convert JSON to CSV at the end
    if success_count > 0:
        convert_json_to_csv()
    else:
        print("No successful analyses to convert to CSV")
    
    return 0

if __name__ == "__main__":
    main()