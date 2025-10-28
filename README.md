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
- 💬 **500K+ Comments Collected** - Processed in ~2 hours
- 📥 **High-Speed Scraping** - ~300K comments/hour (optimizing further)
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
│                    Reddit API (PRAW)                    │
└────────────────┬────────────────────────────────────────┘
                 │
      ┌──────────▼──────────┐
      │  Subreddit Checker  │  (197 countries validated)
      │                     │  (Changeable approval: 100K+ subs, 1000+ comments/week)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │    Post Scraper     │  (Last 7 days, approved subreddits)
      │                     │  (Collects post metadata)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │  Comment Scraper    │  ✅ COMPLETE
      │                     │  (500K+ comments)
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

```
RedditCountryHappinessAnalysis/
├── src/
│   ├── analyzers/              # 🔜 NLP and aggregation
│   │   ├── sentiment_analyzer.py
│   │   └── data_aggregator.py
│   ├── checkers/               # ✅ Subreddit validation
│   │   ├── check_subreddits.py
│   │   └── filter_subreddits.py
│   ├── core/                   # ✅ Core utilities
│   │   ├── connect_reddit.py
│   │   ├── logger.py
│   │   └── config_utils.py
│   ├── scrapers/               # ✅ Data collection
│   │   ├── subreddit_scraper.py
│   │   └── comment_scraper.py
│   ├── utils/                  # ✅ Helper functions
│   │   ├── save_csv.py
│   │   └── subreddit_stats.py
│   └── dashboard/              # 🔜 Visualization
│       └── app.py
├── main.py                     # Main execution pipeline
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

> **⚠️ Important:** `/data` directory is excluded from version control for privacy and data size reasons (contains 1M+ comments). The `.env` file with API credentials is also not included. When forking, you'll need to:
> 1. Set up your own Reddit API credentials in `.env`
> 2. Create the data directory structure manually
> 3. Adjust `config/config.ini` parameters to your needs
>
> This may cause initial setup challenges - this is my first major project and I'm still learning best practices for repository management.

---

## ⚙️ Setup & Installation

> **Note:** Due to missing `/data` directory and `.env` file, this repository is primarily for showcasing the codebase. Running locally requires additional setup.

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

### Configuration

**1. Reddit API Credentials** - Create `.env` in project root:
```env
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
```

**2. Data Directory** - Create the following structure:
```
data/
├── archived/
├── config/
│   └── config.ini
├── dashboard/
├── logs/
├── processed/
├── raw/
│   ├── subreddits/
│   ├── templates/
│   └── weekly_scrapings/
│   │   ├── comments/
│   │   └── posts/
├── processed/
└── logs/
```

**3. Config Settings** - Adjust `config/config.ini` parameters if needed:
```ini
[global]

#scrapig category of subreddits
#parameters : "all", "world", "asia", "africa", "europe", "south_america", "north_america", "oceania"
category = europe

#Scrapes till date - comment_max_days and stops scrapping, default = 7 (one week).
comment_max_days = 7

[check_subreddits]

# If comment count is lower than or equal to this value, the subreddit will be approved and scraping stops (default = 1000).
comment_approve_point = 1000

#If subscriber count is higher than this, subreddit will be approved, default = 100000.
sub_approve_point = 100000

[reddit_post_scraper]

#declare how many post do you want to scrape, default = 750.
post_limit = 750

# If comment count in the post is equals or higher than this, post will be approved, default = 50.
post_comment_approve_limit = 50

[reddit_comment_scraper]

comment_link_limit = 2
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
- **Performance: 500K comments in ~2 hours**

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
| **Scraping Time** | ~2 hours |
| **Average Speed** | ~500,000 comments/hour |
| **Approved Subreddits** | ~40-60 (varies by region/week) |

> **Optimization Note:** Currently working on improving scraping speed through better batching and parallel processing.

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
- **Path Management**: Struggled with relative vs absolute paths; resolved with pathlib
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

- `/data` directory and `.env` not included in repository (requires manual setup)
- No automated testing suite yet
- Dashboard not yet implemented
- Limited to subreddits with sufficient activity (20K+ subscribers)
- Some smaller countries may lack Reddit presence
- Performance bottleneck in single-threaded sections

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
