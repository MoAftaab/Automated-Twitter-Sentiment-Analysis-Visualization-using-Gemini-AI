import os
import subprocess
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv
import glob

load_dotenv()  # This loads the variables from .env file

def install_requirements():
    """Install required packages"""
    print("\nChecking and installing required packages...")
    requirements = [
        'twikit',  # For Twitter scraping
        'openai',  # For GPT API
        'python-dotenv',  # For environment variables
        'pandas',  # For data manipulation
        'matplotlib',  # For visualization
        'seaborn'  # For enhanced visualization
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed/verified successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing {package}: {str(e)}")
            return False
    return True

def run_step(step_name, script_name, expected_output_pattern=None, args=None):
    """Run a Python script and check for successful execution"""
    print(f"\n{'='*50}")
    print(f"Starting {step_name}...")
    print(f"{'='*50}")
    
    # Build command with arguments if provided
    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ {step_name} completed successfully")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    else:
        print(f"✗ Error in {step_name}:")
        print(result.stderr)
        return False

def check_file_exists(filename_pattern, step_name):
    """Check if any file matching the pattern exists"""
    matching_files = glob.glob(filename_pattern)
    if not matching_files:
        print(f"✗ No files matching {filename_pattern} found after {step_name}")
        return False
    return True

def check_env_variables():
    """Check if required environment variables are set"""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("\nMissing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        return False
    return True

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the tweet analysis workflow')
    parser.add_argument('--start-step', type=int, default=1,
                      help='Start from step (1=scrape, 2=clean, 3=gpt, 4=analysis, 5=viz)')
    parser.add_argument('--skip-requirements', action='store_true',
                      help='Skip installing requirements')
    parser.add_argument('--query-file', type=str,
                      help='Name of the query file to use for scraping')
    args = parser.parse_args()

    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Starting workflow run at {timestamp}")
    
    # Define workflow steps with their expected output patterns
    workflow_steps = [
        ("Twitter Scraping", "01_scrape_tweets.py", "01_tweets_*.csv"),
        ("Tweet Cleaning", "02_clean_tweets.py", "02_cleaned_tweets.csv"),
        ("GPT Analysis", "03_analyze_sentiment.py", "03_sentiment_labels.csv"),
        ("Data Analysis", "04_create_analysis.py", "04_data_analysis.csv"),
        ("Data Visualization", "05_generate_visualization.py", "05_sentiment_analysis.png")
    ]
    
    # Step 0: Install requirements only if starting from step 1 and not explicitly skipped
    if args.start_step == 1 and not args.skip_requirements:
        if not install_requirements():
            print("✗ Failed to install required packages")
            return 1
        
    # Check environment variables
    if not check_env_variables():
        print("✗ Please set up required environment variables in .env file")
        return 1
    
    try:
        # Check if starting file exists when not starting from beginning
        if args.start_step > 1:
            input_pattern = workflow_steps[args.start_step - 2][2]
            if not check_file_exists(input_pattern, "previous step"):
                raise Exception(f"Cannot start from step {args.start_step}: No files matching {input_pattern} found")
        
        # Run workflow steps
        for i, (step_name, script_name, output_pattern) in enumerate(workflow_steps, 1):
            if i >= args.start_step:  # Only run steps from the specified starting point
                # For the first step (scraping), handle query file selection
                step_args = []
                if i == 1:  # First step is scrape.py
                    if args.query_file:
                        step_args = ['--query-file', args.query_file]
                    else:
                        print("\nNo query file specified. Please select a query file:")
                        # Run the script directly without capturing output to show interactive menu
                        query_selection = subprocess.run([sys.executable, script_name])
                        if query_selection.returncode != 0:
                            raise Exception("Failed to select query file")
                        # After selection, get the selected file
                        selected_file = glob.glob('01_tweets_*.csv')[-1] if glob.glob('01_tweets_*.csv') else None
                        if not selected_file:
                            raise Exception("No query file was selected")
                        print(f"\nContinuing with selected query file...")
                        # Skip running the step again since we already ran it
                        continue
                
                if not run_step(step_name, script_name, args=step_args):
                    raise Exception(f"Failed at {step_name}")
                if not check_file_exists(output_pattern, step_name):
                    raise Exception(f"No files matching {output_pattern} generated")
        
        print("\n✓ Workflow completed successfully!")
        print(f"Output files generated:")
        for _, _, output_pattern in workflow_steps[args.start_step-1:]:
            matching_files = glob.glob(output_pattern)
            for file in matching_files:
                print(f"- {file}")
        
    except Exception as e:
        print(f"\n✗ Workflow failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 