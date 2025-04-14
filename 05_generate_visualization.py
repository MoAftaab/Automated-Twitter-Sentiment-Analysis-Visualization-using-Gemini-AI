import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import glob
import os

def generate_visualization():
    # Find the most recent analysis file
    analysis_files = glob.glob('04_data_analysis.csv')
    if not analysis_files:
        print("No analysis file found. Please run the analysis step first.")
        return 1
    
    input_file = analysis_files[0]  # There should only be one
    output_file = '05_sentiment_analysis.png'
    
    print(f"Processing {input_file}...")

    # Read the data
    df = pd.read_csv(input_file)
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Create the visualization
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='date', y='score')
    
    # Add horizontal lines for score ranges
    plt.axhline(y=1, color='red', linestyle='--', alpha=0.3)
    plt.axhline(y=2, color='orange', linestyle='--', alpha=0.3)
    plt.axhline(y=3, color='gray', linestyle='--', alpha=0.3)
    plt.axhline(y=4, color='lightgreen', linestyle='--', alpha=0.3)
    plt.axhline(y=5, color='green', linestyle='--', alpha=0.3)
    
    # Add legend for score ranges
    legend_elements = [
        plt.Line2D([0], [0], color='red', lw=2, label='1: Very Unsatisfied'),
        plt.Line2D([0], [0], color='orange', lw=2, label='2: Unsatisfied'),
        plt.Line2D([0], [0], color='gray', lw=2, label='3: Neutral'),
        plt.Line2D([0], [0], color='lightgreen', lw=2, label='4: Satisfied'),
        plt.Line2D([0], [0], color='green', lw=2, label='5: Very Satisfied')
    ]
    
    plt.legend(handles=legend_elements, title='Sentiment Score Range', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.title('Sentiment Analysis Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Visualization saved to {output_file}")
    return 0

if __name__ == "__main__":
    exit(generate_visualization()) 