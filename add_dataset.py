#!/usr/bin/env python3
"""
Script to help users add their own datasets to the sentiment analysis pipeline
"""

import os
import pandas as pd
import shutil
from config import DATASET_CONFIG

def validate_dataset(file_path):
    """Validate that the dataset has the required columns"""
    try:
        df = pd.read_csv(file_path)
        required_columns = ['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"📋 Required columns: {required_columns}")
            print(f"📋 Your columns: {list(df.columns)}")
            return False
        
        print(f"✅ Dataset validation passed!")
        print(f"📊 Found {len(df)} tweets")
        print(f"📋 Columns: {list(df.columns)}")
        return True
        
    except Exception as e:
        print(f"❌ Error reading dataset: {str(e)}")
        return False

def add_dataset():
    """Interactive script to add a new dataset"""
    print("🔄 Add Your Own Dataset")
    print("=" * 50)
    
    # Get file path
    file_path = input("📁 Enter the path to your CSV file: ").strip()
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    # Validate dataset
    if not validate_dataset(file_path):
        return
    
    # Get dataset name
    dataset_name = input("📝 Enter a name for this dataset (e.g., 'my_tweets'): ").strip()
    
    if not dataset_name:
        dataset_name = "custom_dataset"
    
    # Copy file to project directory
    target_filename = f"01_tweets_{dataset_name}.csv"
    target_path = os.path.join(".", target_filename)
    
    try:
        shutil.copy2(file_path, target_path)
        print(f"✅ Dataset copied to: {target_path}")
        
        # Update config (in memory, user needs to manually update config.py)
        print(f"\n📝 To use this dataset, add this line to config.py:")
        print(f'    "{dataset_name}": "{target_filename}",')
        
        print(f"\n🚀 To run analysis with your dataset:")
        print(f"python main.py --start-step 2 --skip-requirements")
        
    except Exception as e:
        print(f"❌ Error copying file: {str(e)}")

def show_example_format():
    """Show example of required CSV format"""
    print("\n📋 Required CSV Format:")
    print("=" * 50)
    example_data = {
        'Tweet_count': [1, 2, 3],
        'Username': ['user1', 'user2', 'user3'],
        'Text': ['Tweet text 1', 'Tweet text 2', 'Tweet text 3'],
        'Created At': ['2025-01-15 10:30:00', '2025-01-15 11:00:00', '2025-01-15 11:30:00'],
        'Retweets': [10, 5, 20],
        'Likes': [50, 25, 100]
    }
    
    df = pd.DataFrame(example_data)
    print(df.to_string(index=False))
    print("\n💡 Make sure your CSV has these exact column names!")

if __name__ == "__main__":
    print("🎯 Dataset Management Tool")
    print("1. Add new dataset")
    print("2. Show required format")
    print("3. List current datasets")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        add_dataset()
    elif choice == "2":
        show_example_format()
    elif choice == "3":
        print("\n📊 Available datasets:")
        for name, path in DATASET_CONFIG.items():
            exists = "✅" if os.path.exists(path) else "❌"
            print(f"  {exists} {name}: {path}")
    else:
        print("❌ Invalid choice")