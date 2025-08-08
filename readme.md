# 🐦 Twitter Sentiment Analysis Pipeline

A complete automated pipeline for analyzing Twitter sentiment using **Google Gemini AI**. Scrape tweets, clean data, analyze sentiment, and generate beautiful visualizations - all with progress tracking!

## ⚠️ Security Notice

- **Never commit API keys** or credentials to the repository
- Store sensitive information in `api_keys.env` file
- The repository includes `.gitignore` to prevent accidental commits
- Keep your Twitter credentials and API keys secure

## ✨ Features

- 🐦 **Twitter scraping** using twikit (optional)
- 🧹 **Automatic data cleaning** and preprocessing
- 🤖 **AI sentiment analysis** using Google Gemini API
- 📊 **Data analysis** and statistical insights
- 📈 **Beautiful visualizations** with charts and graphs
- 📋 **Progress tracking** with real-time progress bars
- 🔄 **Automated workflow** management
- 📁 **Custom dataset support** - use your own data
- ⚡ **Rate limiting** to handle API quotas
- 🎯 **Sentiment scoring** on 1-5 scale

## 🔧 Requirements

- **Python 3.8+**
- **Google Gemini API key** (for AI sentiment analysis)
- **Twitter account** (optional, only for live scraping)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd <repo-name>
pip install -r requirements.txt
```

### 2. Configure API Key

Create `api_keys.env` file:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get your Gemini API key:**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into `api_keys.env`

### 3. Choose Your Workflow

#### 🎯 **Option A: Use Pre-saved Dataset (Recommended)**

```bash
python main.py --start-step 2 --skip-requirements
```

- Uses included sample dataset (20 tweets about grocery prices)
- No Twitter account needed
- Works immediately with just Gemini API key

#### 🐦 **Option B: Scrape Fresh Twitter Data**

```bash
# First, set up Twitter authentication
python 00_setup_auth.py

# Then run full pipeline
python main.py
```

- Scrapes live tweets from Twitter
- Requires Twitter account credentials
- May face account blocking issues

## 📋 Usage Commands

### 🔄 **Complete Workflow Commands**

#### Use Pre-saved Dataset

```bash
python main.py --start-step 2 --skip-requirements
```

#### Scrape Fresh Twitter Data

```bash
python main.py
```

### 📁 **Add Your Own Dataset**

#### Method 1: Interactive Helper

```bash
python add_dataset.py
```

- Validates your CSV format
- Copies file to project directory
- Shows usage instructions

#### Method 2: Manual Replacement

```bash
# Replace the default dataset
cp your_tweets.csv 01_tweets_query_grocery.csv
python main.py --start-step 2 --skip-requirements
```

#### Required CSV Format

Your dataset must have these columns:

```csv
Tweet_count,Username,Text,Created At,Retweets,Likes
1,user1,"Tweet text here",2025-01-15 10:30:00,10,50
2,user2,"Another tweet",2025-01-15 11:00:00,5,25
```

### 🔧 **Individual Step Commands**

```bash
# Step 1: Scrape Twitter (requires auth)
python 01_scrape_tweets.py --query-file query_grocery.txt

# Step 2: Clean data
python 02_clean_tweets.py

# Step 3: Gemini AI sentiment analysis
python 03_analyze_sentiment.py

# Step 4: Data analysis
python 04_create_analysis.py

# Step 5: Generate visualization
python 05_generate_visualization.py
```

### ⚙️ **Command Line Options**

- `--start-step x`: Start from specific step (1-5)
- `--skip-requirements`: Skip installing requirements
- `--query-file`: Specify query file for scraping

## 🏗️ Project Structure

```
.
├── main.py                      # 🎯 Main workflow controller
├── 00_setup_auth.py             # 🔐 Twitter authentication setup
├── 01_scrape_tweets.py          # 🐦 Twitter scraping module
├── 02_clean_tweets.py           # 🧹 Tweet cleaning module
├── 03_analyze_sentiment.py      # 🤖 Gemini AI sentiment analysis
├── 04_create_analysis.py        # 📊 Data analysis module
├── 05_generate_visualization.py # 📈 Visualization generator
├── add_dataset.py               # 📁 Dataset management helper
├── config.py                    # ⚙️ Configuration settings
├── api_keys.env                 # 🔑 API keys (create this)
├── credentials.ini              # 🐦 Twitter credentials (optional)
├── query_*.txt                  # 🔍 Search query files
├── requirements.txt             # 📦 Python dependencies
└── README.md                    # 📖 Documentation
```

## 📊 Output Files

The pipeline generates these files automatically:

| File                        | Description            | Content                               |
| --------------------------- | ---------------------- | ------------------------------------- |
| `01_tweets_*.csv`           | Raw scraped tweets     | Original Twitter data                 |
| `02_cleaned_tweets.csv`     | Cleaned tweets         | Processed and cleaned text            |
| `03_sentiment_labels.csv`   | **Gemini AI analysis** | Sentiment scores (1-5) + explanations |
| `04_data_analysis.csv`      | Combined data          | Tweets + sentiment + timestamps       |
| `05_sentiment_analysis.png` | **Visualization**      | Charts and graphs                     |
| `gpt_analysis.json`         | Raw AI responses       | Detailed Gemini API responses         |

## 🎯 Sentiment Scoring

Gemini AI analyzes each tweet on a **1-5 scale**:

| Score | Label               | Description                       |
| ----- | ------------------- | --------------------------------- |
| **1** | 😡 Very Unsatisfied | Strong anger/outrage about prices |
| **2** | 😞 Unsatisfied      | Complaints/disappointment         |
| **3** | 😐 Neutral          | Balanced/observational            |
| **4** | 😊 Satisfied        | Found deals/improvements          |
| **5** | 😍 Very Satisfied   | Enthusiastic about affordability  |

## 🔐 Setup Requirements

### 🤖 **Gemini API Setup (Required)**

1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Create Key**: Click "Create API Key"
3. **Copy Key**: Save your key securely
4. **Add to Project**: Create `api_keys.env` file:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 🐦 **Twitter Setup (Optional - for live scraping)**

1. **Create `credentials.ini`**:
   ```ini
   [X]
   username = your_twitter_username
   email = your_twitter_email
   password = your_twitter_password
   ```
2. **Run authentication**:
   ```bash
   python 00_setup_auth.py
   ```
3. **Note**: Twitter may block automated scraping

## ⚡ **Rate Limits & Quotas**

### Gemini API Limits (Free Tier)

- **15 requests per minute**
- **Automatic delays**: 4 seconds between requests
- **Upgrade**: For larger datasets, consider paid plan

### Progress Tracking

- ✅ **Real-time progress bar**
- ✅ **Success/failure counts**
- ✅ **Processing speed**
- ✅ **Rate limit handling**

## 🛠️ **Troubleshooting**

### Common Issues

#### "Twitter account blocked"

- **Solution**: Use pre-saved dataset option
- **Command**: `python main.py --start-step 2 --skip-requirements`

#### "Rate limit exceeded"

- **Cause**: Hit Gemini's daily/minute limits
- **Solution**: Wait or upgrade Gemini plan

#### "Invalid API key"

- **Check**: `api_keys.env` file exists and has correct key
- **Format**: `GEMINI_API_KEY=your_key_here`

#### "Dataset not found"

- **Check**: CSV file exists in project directory
- **Use**: `python add_dataset.py` to add your data

## 🎉 **Example Results**

After running the pipeline, you'll get:

- **Sentiment distribution** (e.g., 60% negative, 30% neutral, 10% positive)
- **Time-series analysis** showing sentiment trends
- **Detailed explanations** for each sentiment score
- **Beautiful visualizations** with charts and graphs

## 📚 **Credits & References**

- **Gemini AI**: Google's advanced language model
- **Twikit**: Twitter scraping library
- **Tutorial**: [Scraping X.com with Twikit](https://youtu.be/6D6fVyFQD5A)

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🚀 **Quick Commands Summary**

```bash
# Use pre-saved dataset (recommended)
python main.py --start-step 2 --skip-requirements

# Add your own dataset
python add_dataset.py

# Scrape fresh Twitter data
python main.py

# Individual steps
python 03_analyze_sentiment.py  # Just run sentiment analysis
```

**Need help?** Check the troubleshooting section or create an issue!
