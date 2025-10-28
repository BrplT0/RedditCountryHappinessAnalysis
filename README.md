# 🌍 Reddit Country Happiness Analysis

> A large-scale NLP project analyzing sentiment patterns across European countries through Reddit comments to create an interactive happiness visualization dashboard.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PRAW](https://img.shields.io/badge/PRAW-7.7+-orange.svg)](https://praw.readthedocs.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📊 Project Overview

This project leverages Reddit's vast user-generated content to analyze and visualize happiness trends across European nations. By processing **1 million+ comments** from country-specific subreddits, we aim to create a sentiment-based heatmap showing which regions are happiest based on social media discourse.

> ⚠️ **Note**: This is my first major data engineering project. While functional, there may be areas for optimization and improvement. Feedback and contributions are welcome!

### Current Capabilities

- 🗺️ **150+ Countries Supported** - Scalable to global analysis
- 🇪🇺 **European Focus** - Majority of European countries covered
- 💬 **1M+ Comments Collected** - Processed efficiently
- 📥 **High-Speed Scraping** - ~400K comments/hour (optimized)
- 🔄 **Weekly Automation Ready** - Self-updating data pipeline
- 🤖 **Multi-lingual Support** - Handles 20+ European languages

---

## 🎯 Motivation

Social media platforms contain authentic, unfiltered opinions about daily life, politics, economy, and social issues. By analyzing these conversations at scale, we can:

- Track happiness trends over time
- Compare sentiment across cultures
- Identify regional events' emotional impact
- Provide data-driven insights for researchers and policymakers

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Reddit API (PRAW)                          │
└────────────────┬────────────────────────────────────────┘
                 │
      ┌──────────▼──────────┐
      │  Subreddit Checker  │  (197 countries validated)
      │                     │  (Threshold: 100K+ subs, 1000+ comments/week)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │    Post Scraper     │  (Last 7 days, approved subreddits)
      │                     │  (Collects post metadata)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │  Comment Scraper    │  ✅ COMPLETE
      │                     │  (1M+ comments, 30min for 200K)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │   Preprocessing     │  ⏳ IN PROGRESS
      │                     │  (Spam filter, data cleaning)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │ Sentiment Analysis  │  🔜 PLANNED
      │                     │  (Multi-lingual NLP)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │  Data Aggregation   │  🔜 PLANNED
      │                     │  (Country-level statistics)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │  Streamlit Dashboard│  🔜 PLANNED
      │                     │  (Interactive choropleth map)
      └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9+** - Core language
- **PRAW 7.7+** - Reddit API wrapper with rate limiting
- **Pandas** - Data manipulation and CSV processing
- **Multiprocessing** - Parallel execution for performance
- **Dotenv** - Environment variable management for secrets

### Data Collection
- **Custom Scrapers** - Post and comment collection
- **Approval System** - Quality filtering (subscriber/activity thresholds)
- **Logging System** - Comprehensive activity tracking

### Planned NLP & Visualization
- **TextBlob** / **XLM-RoBERTa** - Sentiment analysis (evaluating options)
- **Streamlit** - Interactive web dashboard
- **Plotly** - Choropleth map visualization

### Infrastructure
- **ConfigParser** - Configuration management
- **Pathlib** - Cross-platform path handling
- **Custom Logger** - File and console logging

---

## 📂 Project Structure

This project follows a standardized architecture separating configuration, assets, source code, and data.

```
RedditCountryHappinessAnalysis/
├── assets/
│   ├── subreddits.csv            # 🔒 Populated list (Ignored by Git)
│   └── subreddits.template.csv   # ✅ Public template (Tracked by Git)
├── config/
│   └── config.ini                # ✅ Public settings (Tracked by Git)
├── data/                          # 🔒 Generated outputs (Ignored by Git)
│   ├── archived/
│   ├── dashboard/
│   ├── logs/
│   ├── processed/
│   ├── raw/
│   └── weekly_scrapings/
├── src/
│   ├── analyzers/                # 🔜 NLP and aggregation
│   ├── checkers/                 # ✅ Subreddit validation
│   ├── core/                     # ✅ Core utilities
│   ├── scrapers/                 # ✅ Data collection
│   ├── utils/                    # ✅ Helper functions
│   └── dashboard/                # 🔜 Visualization
├── .env                          # 🔒 API secrets (Ignored by Git)
├── main.py                       # Main execution pipeline
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

> **Note on Project Setup:**
>
> This repository is configured for easy setup, but requires manual folder creation.
> - The `/data` directory is **entirely ignored by Git**. You **must** create the `/data` folder and its subdirectories (`raw`, `logs`, `processed`, etc.) manually for the scripts to run.
> - You **must** manually create the `.env` file for your API keys.
> - You **must** manually create the `assets/subreddits.csv` file from the provided template.

---

## ⚙️ Setup & Installation

> **Note:** Running locally requires you to provide your own API credentials, subreddit list, and data folder structure.

### Prerequisites
- Python 3.9 or higher
- Reddit API credentials ([Get them here](https://www.reddit.com/prefs/apps))
- 6GB+ RAM recommended for large-scale processing

### Installation

```bash
# Clone the repository
git clone https://github.com/BrplT0/RedditCountryHappinessAnalysis.git
cd RedditCountryHappinessAnalysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration (Required Steps)

**1. Reddit API Credentials (Secrets)**

Create a `.env` file in the project root:

```env
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
```

**2. Subreddit List (Input Data)**

The code needs `assets/subreddits.csv` to run. Create this file by duplicating the template:

```bash
# On Linux/macOS
cp assets/subreddits.template.csv assets/subreddits.csv

# On Windows
copy assets\subreddits.template.csv assets\subreddits.csv
```

Now, **edit `assets/subreddits.csv`** and populate it with the subreddits you want to analyze.

**3. Data Directory (Critical Step)**

You **must** manually create the `data/` folder structure that the scripts expect. Create these folders in the project root:

```bash
mkdir -p data/archived
mkdir -p data/dashboard
mkdir -p data/logs
mkdir -p data/processed
mkdir -p data/raw/subreddits
mkdir -p data/weekly_scrapings/comments
mkdir -p data/weekly_scrapings/posts
```

**4. General Settings (Public)**

Adjust parameters in `config/config.ini` as needed. The defaults are sensible:

```ini
[global]
# Scraping category of subreddits
# Parameters: "all", "world", "asia", "africa", "europe", "south_america", "north_america", "oceania"
category = europe

# Scrapes till date - comment_max_days and stops scraping, default = 7 (one week)
comment_max_days = 7

[check_subreddits]
# ... (and other settings) ...
```

---

## 🚀 Current Status & Usage

### Completed Modules ✅

**1. Subreddit Validation**

```bash
python -m src.checkers.check_subreddits
```

- Validates 197 country subreddits
- Checks subscriber count (>20K threshold)
- Analyzes activity (>50 comments/week)
- Outputs approved subreddits for scraping

**2. Post Collection**

```bash
python -m src.scrapers.subreddit_scraper
```

- Scrapes posts from approved subreddits
- Collects last 7 days of content
- Stores post metadata (title, score, comments count)

**3. Comment Collection**

```bash
python -m src.scrapers.comment_scraper
```

- Post ID-based comment extraction
- Nested thread support
- **Performance: 200K comments in ~30 minutes** (~400K/hour)

### Full Pipeline (Current State)

```bash
python main.py
```

Executes:
1. ✅ Subreddit validation
2. ✅ Post scraping
3. ✅ Comment collection
4. ⏳ Data preprocessing (in development)

---

## 📈 Performance Metrics

| Metric | Current Performance |
|--------|---------------------|
| **Countries Supported** | 150+ (Global capability) |
| **Active Focus** | Majority of European countries |
| **Comments Collected** | 1,000,000+ |
| **Scraping Time** | ~30 minutes for 200K comments |
| **Average Speed** | ~400,000 comments/hour |
| **Approved Subreddits** | ~40-60 (varies by region/week) |

> **Performance Achievement:** Recently collected 200K comments in just 30 minutes through optimized batching and parallel processing!

---

## 🧠 Planned Sentiment Analysis

### Data Cleaning Strategy

- Remove `[deleted]` and `[removed]` comments
- Filter bot accounts and AutoModerator
- Eliminate comments < 10 characters
- Handle special characters and emojis

### Multi-lingual NLP Options (Under Evaluation)

**Option A: TextBlob**
- Fast processing (~10K comments/min)
- Basic accuracy, good for prototyping
- Works across multiple languages

**Option B: XLM-RoBERTa**
- High accuracy for 100+ languages
- Requires GPU for reasonable speed
- Pre-trained on social media text

**Option C: Language-Specific Models**
- Best accuracy per language
- Complex pipeline management
- Higher maintenance overhead

### Sentiment Scoring System (Planned)

| Score | Category | Emoji |
|-------|----------|-------|
| 0.5 to 1.0 | Very Positive | 😄 |
| 0.05 to 0.5 | Positive | 🙂 |
| -0.05 to 0.05 | Neutral | 😐 |
| -0.5 to -0.05 | Negative | 😟 |
| -1.0 to -0.5 | Very Negative | 😢 |

---

## 📊 Planned Dashboard Features

### Interactive Visualizations

- **Choropleth World Map**: Countries colored by happiness score
- **Time Series Analysis**: Weekly/monthly trend tracking
- **Country Rankings**: Top happiest/unhappiest nations
- **Sentiment Distribution**: Pie charts showing positive/neutral/negative ratios
- **Word Clouds**: Most discussed topics per country

### Technologies

- **Streamlit**: Rapid dashboard prototyping
- **Plotly**: Interactive maps and charts
- **Pandas**: Data aggregation and filtering

---

## 🎓 Key Learnings & Challenges

### Technical Achievements

- ✅ Handled 500K+ records efficiently with memory-conscious design
- ✅ Optimized Reddit API usage within rate limits (60 requests/min)
- ✅ Built modular, maintainable codebase with separation of concerns
- ✅ Implemented robust logging and error handling

### Challenges Encountered

- **Rate Limiting**: Learned to batch requests and implement smart delays
- **Path Management**: Struggled with relative vs absolute paths; **resolved with pathlib & root-level folders**
- **Data Volume**: Initial memory issues; solved with streaming writes and batch processing
- **Multi-stage Pipeline**: Coordinating multiple scripts; created main.py orchestrator

### Skills Developed

- Large-scale data collection and ETL pipelines
- API optimization and rate limit management
- Python project architecture and modularity
- Git version control and documentation
- Problem-solving under constraints (API limits, memory)

### Areas for Improvement

- More efficient data structures for faster processing
- Better exception handling in edge cases
- Unit tests for critical functions
- Performance profiling and optimization

---

## 🔮 Roadmap

### Short-term (Next Steps)

- [ ] Complete data preprocessing module
- [ ] Implement sentiment analysis (choosing between TextBlob/XLM-RoBERTa)
- [ ] Build data aggregation pipeline
- [ ] Create basic Streamlit dashboard

### Medium-term

- [ ] Expand beyond Europe to global coverage
- [ ] Optimize scraping speed (target: <1 hour for 500K comments)
- [ ] Add time series analysis
- [ ] Implement automated weekly updates

### Long-term (Future Enhancements)

- [ ] Real-time streaming dashboard
- [ ] Correlation analysis with geopolitical events
- [ ] API endpoint for third-party access
- [ ] Mobile-responsive interface
- [ ] Predictive modeling for happiness trends

---

## 🐛 Known Issues & Limitations

- **Requires Manual Setup**: `/data` directory, `.env` file (for API keys), and `assets/subreddits.csv` (for input data) must be created manually
- **No Test Suite**: No automated testing suite yet
- **Dashboard Pending**: Dashboard not yet implemented
- **Data Scarcity**: Limited to subreddits with sufficient activity (20K+ subscribers). Some smaller countries may lack Reddit presence
- **Performance**: Bottlenecks exist in single-threaded sections (under review)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Berat Polat**

- GitHub: [@BrplT0](https://github.com/BrplT0)
- LinkedIn: [Berat Polat](https://www.linkedin.com/in/berat-polat-923093249)
- Email: beratpolat0402@gmail.com

---

## 🙏 Acknowledgments

- **Reddit & PRAW**: For comprehensive API access and excellent documentation
- **HuggingFace**: For pre-trained NLP models and transformers library
- **Streamlit Community**: For making data visualization accessible

---

## 📞 Contact & Contributions

This is my first major data project, and I'm learning as I build. Feedback, suggestions, and contributions are highly appreciated!

- **Issues**: [GitHub Issues](https://github.com/BrplT0/RedditCountryHappinessAnalysis/issues)
- **Pull Requests**: Welcome! Please open an issue first to discuss major changes
- **Email**: beratpolat0402@gmail.com

---

<div align="center">

### ⭐ If you find this project interesting, please consider starring it!

**Status**: 🚧 Active Development | 📊 Data Collection Complete | 🤖 NLP In Progress

Built with ❤️ and ☕ | Learning by doing

</div>