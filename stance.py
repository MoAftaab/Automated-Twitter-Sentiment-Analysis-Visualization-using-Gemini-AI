import pandas as pd
import numpy as np
from textblob import TextBlob

# Load the dataset
df = pd.read_csv('cleaned_tweets.csv')

# Sample 10 tweets randomly
sample_df = df.sample(10, random_state=42).copy()

# Define a function to map polarity to a 5-point stance scale
def polarity_to_stance(polarity):
    if polarity <= -0.6:
        return 1  # Very Negative
    elif -0.6 < polarity <= -0.2:
        return 2  # Negative
    elif -0.2 < polarity <= 0.2:
        return 3  # Neutral
    elif 0.2 < polarity <= 0.6:
        return 4  # Positive
    else:
        return 5  # Very Positive

# Apply stance classification to all tweets
df["polarity"] = df["tweet_content"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
df["stance_score"] = df["polarity"].apply(polarity_to_stance)

# Apply the same to our sample for verification
sample_df["polarity"] = sample_df["tweet_content"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
sample_df["stance_score"] = sample_df["polarity"].apply(polarity_to_stance)

# Display the sample with assigned stance scores
print(sample_df[["tweet_content", "polarity", "stance_score"]])

# Calculate distribution of stances
stance_distribution = df['stance_score'].value_counts(normalize=True) * 100
print("\nStance Distribution (%):")
print(stance_distribution)

# Save results to a new CSV
df.to_csv('tweets_with_stance.csv', index=False)