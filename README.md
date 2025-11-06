# 🌍 Reddit Country Happiness Analysis

> A high-throughput data pipeline that scrapes, processes, and analyzes Reddit comments to create an interactive happiness visualization dashboard.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![PRAW](https://img.shields.io/badge/PRAW-7.7+-orange.svg)](https://praw.readthedocs.io/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.x-yellow.svg)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📊 Project Overview

This project leverages Reddit's vast user-generated content to analyze and visualize global happiness trends. By processing **hundreds of thousands of comments** weekly, we create a sentiment-based interactive dashboard showing which regions are happiest based on social media discourse.

### 🎯 Current Status: **Ready for Deployment**

The complete pipeline is **production-ready**, featuring:

- 🗺️ **Interactive Choropleth Map** - Global happiness heatmap
- 📈 **Time Series Analysis** - Track happiness trends over time
- 🏆 **Top/Bottom Rankings** - Happiest and unhappiest countries
- 🌐 **150+ Countries** - Comprehensive global coverage

---

## ✨ Key Features

- 🚀 **High-Throughput Scraper** - Optimized API usage with capacity of **~500,000 comments/hour**
- 🎯 **Geographic Filtering** - Target specific regions or analyze global data
- ⚙️ **Flexible Backend** - Config-switchable between CPU multiprocessing and GPU acceleration
- 🤖 **Dual NLP Models** - Choose between XLM-RoBERTa (accurate) or DistilBERT (fast)
- 🔧 **Highly Configurable** - Fine-tune scraping depth, approval thresholds, and time windows
- ♻️ **Smart Caching** - Re-runnable pipeline skips redundant processing
- 📦 **Efficient Archival** - Historical data compressed and preserved

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Reddit API (PRAW)                        │
└────────────────┬────────────────────────────────────────┘
                 │
      ┌──────────▼──────────┐
      │  Subreddit Checker  │  ✅ COMPLETE
      │                     │  (Validates 197 countries)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │    Post Scraper     │  ✅ COMPLETE
      │                     │  (Scrapes posts from last 7 days)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │  Comment Scraper    │  ✅ COMPLETE
      │                     │  (Capacity: ~500K/hour)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │   Preprocessing     │  ✅ COMPLETE
      │                     │  (RegEx cleaning, bot/spam filtering)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │ Sentiment Analysis  │  ✅ COMPLETE
      │                     │  (XLM-R, CPU/GPU compatible)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │  Data Aggregation   │  ✅ COMPLETE
      │                     │  (Country-level statistics)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │  Streamlit Dashboard│  ✅ COMPLETE
      │                     │  (Interactive visualization)
      └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Core Pipeline
- **Python 3.12** - Core language
- **PRAW 7.7+** - Reddit API Wrapper
- **Pandas** - Data manipulation and ETL
- **NumPy** - Data chunking for multiprocessing

### NLP & Performance
- **Hugging Face `transformers`** - XLM-RoBERTa model
- **PyTorch (`torch`)** - ML backend (CPU/GPU)
- **`multiprocessing`** - Parallel processing on CPU

### Visualization
- **Streamlit** - Interactive web dashboard
- **Plotly** - Choropleth & time series visualization

### Configuration & Security
- **`configparser`** - Settings management
- **`python-dotenv`** - Environment variable handling
- **`logging`** - Multiprocessing-safe logging

---

## 📂 Project Structure

```
RedditCountryHappinessAnalysis/
├── assets/
│   ├── subreddits.csv            # 🔒 Populated list (Ignored by Git)
│   └── subreddits.template.csv   # ✅ Public template (Tracked by Git)
├── config/
│   └── config.ini                # ✅ Public settings (Tracked by Git)
├── data/                          # 🔒 Generated outputs (Ignored by Git)
│   ├── archived/                  # Compressed historical data
│   ├── dashboard/                 # Current dashboard data
│   ├── logs/                      # Pipeline execution logs
│   ├── processed/                 # Cleaned and analyzed data
│   ├── raw/                       # Raw scraped comments
│   └── weekly_scrapings/          # Weekly scraping results
├── src/
│   ├── analyzers/                # ✅ NLP and Aggregation
│   ├── checkers/                 # ✅ Subreddit validation
│   ├── core/                     # ✅ Core utilities (Logger, Config)
│   ├── scrapers/                 # ✅ Data collection
│   ├── utils/                    # ✅ Helper functions
│   └── dashboard/                # ✅ Streamlit visualization
├── .env.example                  # ✅ API Key template
├── main.py                       # Main execution pipeline
├── requirements.txt              # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Setup & Installation

> **Note:** The project automatically creates the `/data` directory structure on first run. You only need to configure API keys and the subreddit list.

### Prerequisites
- **Python 3.11 or 3.12** (3.12 for CPU-only, 3.11 recommended for GPU/CUDA)
- Reddit API credentials
- **16GB+ RAM** (Recommended for CPU multiprocessing on large datasets)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/BrplT0/RedditCountryHappinessAnalysis.git
cd RedditCountryHappinessAnalysis

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install core dependencies
pip install -r requirements.txt
# This installs the CPU-only version of PyTorch by default.
```

### Configuration (Required Steps)

**1. Create `.env` file (API Secrets)**

Rename `.env.example` to `.env` and add your Reddit API keys.

```bash
# On Linux/Mac:
mv .env.example .env

# On Windows:
ren .env.example .env

# Now edit the .env file with your credentials
```

**2. Create `subreddits.csv` (Input Data)**

Rename `subreddits.template.csv` to `subreddits.csv`. The template includes example subreddits.

```bash
# On Linux/Mac:
mv assets/subreddits.template.csv assets/subreddits.csv

# On Windows (CMD):
cd assets
ren subreddits.template.csv subreddits.csv
cd ..

# Edit the file if you want to add/remove subreddits
```

**3. Configure `config.ini` (Pipeline Settings)**

Open `config/config.ini` to customize the pipeline behavior. The configuration file is divided into multiple sections:

```ini
[global]
# Geographic scope: "all", "world", "asia", "africa", "europe", 
# "south_america", "north_america", "oceania"
category = europe

# Scraping lookback period (days)
comment_max_days = 7

[check_subreddits]
# Minimum comments required for subreddit approval
comment_approve_point = 1000

# Minimum subscribers required
sub_approve_point = 100000

[reddit_post_scraper]
# Max posts per subreddit
post_limit = 150

# Minimum comments per post to process
post_comment_approve_limit = 50

[reddit_comment_scraper]
# Comment depth limit (32 = optimal balance)
# 0 = top-level only, None = all (causes rate limits)
comment_link_limit = 32

[analysis]
# Hardware selection: "cpu" or "gpu"
device_type = cpu

# CPU cores (only used if device_type = cpu)
cpu_cores = 4

# Model selection: "roberta" (accurate, 1.6GB) or "distilbert" (faster, 0.5GB)
model_name = distilbert
```

> **Note:** The `/data` directory structure will be **automatically created** by the project when you first run `main.py`.

### (Optional) Setup for GPU (NVIDIA/CUDA)

If you want to use an NVIDIA GPU for faster analysis:

1. Ensure you are using **Python 3.11 or 3.12** (3.11 recommended for CUDA compatibility)
2. Uninstall the CPU-only `torch`:
   ```bash
   pip uninstall torch
   ```
3. Install CUDA-enabled PyTorch (e.g., CUDA 12.1):
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```
4. Update `config.ini`:
   ```ini
   [analysis]
   device_type = gpu
   model_name = distilbert  # Recommended for GPUs with <4GB VRAM
   ```

> **GPU Requirements:** Minimum 3GB VRAM recommended. XLM-RoBERTa requires ~1.6GB, DistilBERT requires ~0.5GB.

---

## 🚀 Usage

### Run the Complete Pipeline

```bash
python main.py
```

The script is **re-runnable**. If it finds already processed data from today (`cleaned_comments.csv`), it will skip the ~20-min scraping/cleaning steps and jump straight to the analysis.

### Run Dashboard Only

```bash
streamlit run src/dashboard/app.py
```

---

## 📈 Performance Benchmarks (Local Machine)

### Scraping Performance
- **~500,000 comments/hour** with optimized API usage
- **Comment depth:** 32 levels captures 99.9% of data without rate limits
- **Geographic filtering:** Reduces processing time by targeting specific regions

### NLP Analysis Performance

**CPU Mode (Ryzen 5 8400F, 6 Cores)**
- **XLM-RoBERTa:**
  - 10,000 comments (Single-Core, `batch_size=64`): ~6 min 17 sec
  - 14,000 comments (`Pool(4)`): ~21 minutes
- **DistilBERT:** (Estimated 2-3x faster than RoBERTa)
  
> *Note: Benchmarks on Windows with small datasets. Multiprocessing overhead is significant for small volumes. Linux performance with larger datasets will show greater parallelization benefits.*

**GPU Mode**
- **NVIDIA MX350 (2GB VRAM):**
  - XLM-RoBERTa: ❌ `OutOfMemoryError` (model 1.6GB + batch data exceeds VRAM)
  - DistilBERT: ✅ Expected to work (0.5GB model footprint)
- **Recommended GPU:** 3GB+ VRAM (e.g., T4, RTX 3060) for XLM-RoBERTa

### Model Comparison

| Model | VRAM Usage | CPU Speed | Accuracy | Recommended For |
|-------|------------|-----------|----------|-----------------|
| **XLM-RoBERTa** | ~1.6GB | Baseline | High | High-accuracy analysis, powerful GPUs |
| **DistilBERT** | ~0.5GB | 2-3x faster | Good | Production VDS, limited resources |

---

## 🎓 Key Learnings & Challenges

### Technical Achievements

**1. Advanced Configuration System**
- Built a comprehensive multi-section config supporting geographic filtering, threshold tuning, and hardware selection
- Implemented dual-model support (XLM-RoBERTa vs DistilBERT) for different performance/accuracy tradeoffs
- Designed optimal comment depth limit (32 levels) to capture 99.9% of data without hitting API rate limits

**2. Hardware Optimization**
- Diagnosed GPU memory limitations: 2GB VRAM insufficient for XLM-RoBERTa (1.6GB model + batch data)
- Validated DistilBERT as efficient alternative (0.5GB VRAM) for resource-constrained environments
- Optimized CPU multiprocessing as reliable path for production VDS deployment

**3. Robust Error Handling**
- `TypeError: NoneType`: Implemented `.fillna()` before processing API responses
- `IndexError: 512`: Added `truncation=True, max_length=512` to handle token limits
- `AssertionError: Torch not compiled`: Resolved CUDA vs CPU package compatibility

**4. Pipeline Efficiency**
- Idempotent design: Script checks for existing data, skips 20+ min scraping if present
- Balanced scraping strategy: `comment_link_limit=32` avoids rate limits while maximizing data capture
- Multiprocessing logging: Custom logger with `MainProcess` check prevents duplicate entries

**5. Atomic Writes for Live Dashboard**
- Solved data conflict (race condition) between the weekly pipeline (Writer) and the 7/24 dashboard (Reader). 
- Implemented shutil.move to atomically swap .tmp files, ensuring the dashboard never reads a partially written CSV and never crashes.
---

## 🔮 Roadmap

### ✅ Completed
- [x] Subreddit validation system
- [x] High-throughput post & comment scraper
- [x] Preprocessing pipeline (cleaning, filtering)
- [x] Multilingual sentiment analysis (XLM-RoBERTa)
- [x] Country-level data aggregation
- [x] Interactive Streamlit dashboard with choropleth map, time series, and rankings

### 🚀 Next Steps: Deployment
- [ ] Docker containerization
- [ ] VDS deployment with automated weekly cronjob
- [ ] Production monitoring and logging

### 🔜 Future Enhancements
- [ ] Custom frontend development (replacing Streamlit)
- [ ] Database migration evaluation (MongoDB or similar)
- [ ] Email notification system for pipeline failures
- [ ] Advanced time series forecasting
- [ ] Multi-language UI support
- [ ] API endpoint for data access
- [ ] Mobile-responsive frontend
- [ ] Historical data comparison tools
- [ ] Sentiment trend predictions
- [ ] Regional analysis (sub-national level)

---

## 🐛 Known Issues & Limitations

- **No Test Suite**: Lacks automated unit tests (e.g., `pytest`)
- **Manual Monitoring**: Production monitoring system not yet implemented
- **CSV Storage**: May need database migration for long-term scalability

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Berat Polat**

- GitHub: [@BrplT0](https://github.com/BrplT0)
- LinkedIn: [Berat Polat](https://www.linkedin.com/in/berat-polat-923093249)

---

<div align="center">

### ⭐ If you find this project interesting, please consider starring it!

**Status**: 🚀 Ready for Deployment | 📊 Pipeline Complete | 🤖 NLP Optimized

Built with ❤️ and ☕ | Learning by doing

</div>