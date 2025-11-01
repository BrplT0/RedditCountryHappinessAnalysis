# 🌍 Reddit Country Happiness Analysis

> A configurable, high-throughput data pipeline that scrapes, processes, and analyzes Reddit comments to create an interactive happiness visualization dashboard.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![PRAW](https://img.shields.io/badge/PRAW-7.7+-orange.svg)](https://praw.readthedocs.io/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.x-yellow.svg)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📊 Project Overview

This project leverages Reddit's vast user-generated content to analyze and visualize happiness trends. By processing **hundreds of thousands of comments** weekly, we aim to create a sentiment-based heatmap showing which regions are happiest based on social media discourse.

> ⚠️ **Note**: This is a major data engineering project. The core pipeline (scraping, cleaning, and NLP analysis) is complete and functional on a local machine. The next steps involve aggregation and visualization.

### Current Capabilities

- 🗺️ **150+ Countries Supported** - Scalable to global analysis
- 🚀 **High-Throughput Scraper** - Optimized API usage with a capacity of **~500,000 comments/hour**
- ⚙️ **Config-Switchable Backend** - The `config.ini` file allows dynamic switching between:
  - **CPU Mode:** Uses `multiprocessing.Pool` for parallel analysis (e.g., on a Ryzen 5 CPU)
  - **GPU Mode:** Uses an NVIDIA GPU (CUDA) for rapid analysis
- 🤖 **High-Accuracy NLP** - Uses the `XLM-RoBERTa` multilingual model
- ♻️ **Re-runnable Pipeline** - `main.py` checks if data is already processed, skipping 20+ min of scraping if files exist

---

## 🏗️ Architecture (Pipeline Status)

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
      │  Data Aggregation   │  ⏳ IN PROGRESS
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

### Core Pipeline
- **Python 3.12** - Core language
- **PRAW 7.7+** - Reddit API Wrapper
- **Pandas** - Data manipulation and ETL
- **NumPy** - Data chunking for multiprocessing

### NLP & Performance
- **Hugging Face `transformers`** - For loading the XLM-RoBERTa model
- **PyTorch (`torch`)** - The backend for running the NLP model (CPU or GPU)
- **`multiprocessing`** - Used for parallelizing the NLP analysis on CPU

### Infrastructure & Config
- **`configparser`** - Manages settings (API keys, paths, CPU/GPU mode)
- **`python-dotenv`** - Secures API credentials in a `.env` file
- **`logging`** - Custom logger configured for multiprocessing (`MainProcess` check)

### Visualization (Planned)
- **Streamlit** - Interactive web dashboard
- **Plotly** - Choropleth map visualization

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
│   ├── analyzers/                # ✅ NLP and Aggregation
│   ├── checkers/                 # ✅ Subreddit validation
│   ├── core/                     # ✅ Core utilities (Logger, Config)
│   ├── scrapers/                 # ✅ Data collection
│   ├── utils/                    # ✅ Helper functions (SaveCSV, Cleaners)
│   └── dashboard/                # 🔜 Visualization
├── .env.example                  # ✅ API Key template
├── main.py                       # Main execution pipeline
├── requirements.txt              # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

> **Note on Project Setup:**
> - The `/data` directory is **automatically created** by the project on first run.
> - API keys (`.env`) and the subreddit list (`assets/subreddits.csv`) must be renamed from their `.example` / `.template` files.

---

## ⚙️ Setup & Installation

> **Note:** The project automatically creates the `/data` directory structure on first run. You only need to configure API keys and the subreddit list.

### Prerequisites
- **Python 3.11 or 3.12** (3.12 for CPU-only, 3.11 recommended for GPU/CUDA)
- Reddit API credentials
- **16GB+ RAM** (Recommended for CPU `multiprocessing` analysis on large datasets)

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

**3. Configure `config.ini` (CPU/GPU Selection)**

Open `config/config.ini`. The default settings will run the analysis using CPU (`multiprocessing`).

```ini
[analysis]
# "cpu" (default) or "gpu" (NVIDIA)
device_type = cpu
# Cores to use if device_type is "cpu"
cpu_cores = 4 
```

> **Note:** The `/data` directory structure will be **automatically created** by the project when you first run `main.py`.

### (Optional) Setup for GPU (NVIDIA/CUDA)

If you want to use your local NVIDIA GPU (much faster):

1. Ensure you are using **Python 3.11 or 3.12** (3.11 is recommended for maximum CUDA compatibility)
2. Uninstall the CPU-only `torch` from `requirements.txt`:
   ```bash
   pip uninstall torch
   ```
3. Install the CUDA-enabled version (e.g., CUDA 12.1):
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```
4. Change `config.ini` to `device_type = gpu`

---

## 🚀 Full Pipeline Usage

Once setup is complete, run the entire pipeline:

```bash
python main.py
```

The script is **re-runnable**. If it finds already processed data from today (`cleaned_comments.csv`), it will skip the ~20-min scraping/cleaning steps and jump straight to the analysis.

---

## 📈 Performance Benchmarks (Local Machine)

- **Scraping:** ~500,000 comments/hour
- **NLP (XLM-R Model):**
  - **CPU (Ryzen 5 8400F, 6 Cores):**
    - 10,000 comments (Single-Core `batch_size=64`): **~6 minutes 17 seconds** (377s)
    - 14,000 comments (`Pool(4)`): **~21 minutes**
    - *Note: These benchmarks were tested on Windows with relatively small datasets. The multiprocessing overhead is significant for small data volumes. Performance metrics will be updated when tested on Linux with larger datasets where the 4-core parallelization advantage becomes more apparent.*
  - **GPU (NVIDIA MX350, 2GB VRAM):**
    - **Test Failed.** `torch.OutOfMemoryError`. The 2GB VRAM is insufficient to hold the 1.6GB XLM-RoBERTa model *and* the analysis batch data
    - *Conclusion: A GPU with >2GB VRAM (e.g., T4, 3060) is required for GPU mode*

---

## 🎓 Key Learnings & Challenges

- **Hardware Bottlenecks:** Diagnosed critical performance issues. Learned that the heavy (1.6GB) XLM-RoBERTa model **cannot run on a 2GB VRAM GPU (MX350)** due to `OutOfMemoryError`. This confirmed that CPU `multiprocessing` is the most viable path for this hardware.
- **Robust Error Handling:** Solved critical pipeline-breaking errors:
  - **`TypeError: NoneType`**: Handled `None` values from the API using `.fillna()` *before* processing
  - **`IndexError: 512`**: Solved model token limit errors by adding `truncation=True` and `max_length=512` to the `pipeline`
  - **`AssertionError: Torch not compiled`**: Solved by installing the correct `torch` (CUDA vs CPU) package for the Python version
- **Idempotent Pipeline:** Made the `main.py` script "re-runnable" by adding an `if .exists()` check, saving 20+ minutes of scraping/cleaning time if data is already present
- **Multiprocessing Logging:** Re-wrote `logger.py` to check for `MainProcess` to prevent duplicate log entries from each worker process in the `Pool`

---

## 🔮 Roadmap

- [✅] Step 1: Subreddit Checker
- [✅] Step 2: Post Scraper
- [✅] Step 3: Comment Scraper
- [✅] Step 4: Preprocessing (Cleaning)
- [✅] Step 5: Sentiment Analysis (NLP)
- [⏳] **Step 6: Data Aggregation (`groupby`)**
- [🔜] **Step 7: Dashboard (Streamlit + Plotly)**
- [ ] Automate with `cronjob` (VDS/Server) or Windows Task Scheduler (Local)
- [ ] Expand to global subreddits

---

## 🐛 Known Issues & Limitations

- **No Test Suite**: Lacks automated unit tests (e.g., `pytest`)
- **Dashboard Pending**: Visualization is not yet implemented

---

## 👤 Author

**Berat Polat**

- GitHub: [@BrplT0](https://github.com/BrplT0)
- LinkedIn: [Berat Polat](https://www.linkedin.com/in/berat-polat-923093249)

---

<div align="center">

### ⭐ If you find this project interesting, please consider starring it!

**Status**: 🚧 Deployment Planning | 📊 Pipeline Complete | 🤖 NLP Optimized

Built with ❤️ and ☕ | Learning by doing

</div>