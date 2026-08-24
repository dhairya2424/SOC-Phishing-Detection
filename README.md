# 🛡️ SOC Phishing Detection System

> **B2B Security Software** — Real-time URL threat analysis powered by ensemble machine learning.

A Security Operations Center (SOC) tool that detects phishing URLs using multiple ML models with an intuitive Streamlit-based dashboard. Designed as a **B2B solution** for security teams to investigate suspicious URLs — individually or in bulk.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Multi-Model Detection** | Logistic Regression, Random Forest, and XGBoost run in parallel |
| **Single URL Analysis** | Paste any URL and get an instant phishing verdict with confidence scores |
| **Batch Investigation** | Upload a CSV of URLs to scan hundreds of links at once |
| **Adjustable Thresholds** | Fine-tune detection sensitivity per model via sidebar controls |
| **Structural Evidence** | View extracted features — domain info, TLD risk, keyword hits, brand similarity |
| **Exportable Reports** | Download batch scan results as CSV for SOC documentation |
| **Dark Glassmorphism UI** | Modern, professional dashboard built for security analysts |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/SOC-Phishing-Detection.git
cd SOC-Phishing-Detection

# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\Activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📂 Project Structure

```
SOC-Phishing-Detection/
├── app.py                              # Streamlit web application
├── models_new/                         # Trained ML models
│   ├── tfidf.pkl                       # TF-IDF vectoriser
│   ├── logistic.pkl                    # Logistic Regression classifier
│   ├── rf.pkl                          # Random Forest classifier
│   ├── xgb.pkl                         # XGBoost classifier
│   └── thresholds.pkl                  # Optimised decision thresholds
├── Phishing_Detection_Final.ipynb      # Model training notebook
├── Dataset_Builder_Final.ipynb         # Dataset construction notebook
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

---

## 🧠 How It Works

### Feature Engineering
The system extracts **two types of features** from each URL:

1. **TF-IDF Features** — Character-level n-gram vectorisation of the raw URL string, fed to Logistic Regression.
2. **Structural / Lexical Features** — Hand-engineered signals including:
   - URL length, dot count, hyphen count, digit count
   - IP-based hostname detection
   - Phishing keyword score (login, verify, secure, etc.)
   - Brand name similarity (Google, PayPal, Amazon, etc.)
   - Risky TLD detection (.tk, .ml, .ga, etc.)
   - Subdomain count

### Models
| Model | Feature Input | Purpose |
|---|---|---|
| Logistic Regression | TF-IDF vectors | Fast baseline, captures character-level patterns |
| Random Forest | Structural features | Ensemble of decision trees for robust classification |
| XGBoost | Structural features | Gradient-boosted trees for high accuracy |

Each model outputs a **phishing probability** (0–1). The active model's probability is compared against a configurable threshold to produce the final verdict.

---

## 📊 Usage

### Single URL Investigation
1. Select a model and threshold from the sidebar
2. Paste a URL in the **Single URL Investigation** tab
3. Click **⚡ Analyse URL**
4. View the verdict, model comparison table, and structural evidence

### Batch Investigation
1. Prepare a CSV file with a column named `url`
2. Upload it in the **Batch Investigation** tab
3. Click **🚀 Start Batch Scan**
4. Review the summary metrics, filter results, and download the report

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) with custom CSS
- **ML Models**: scikit-learn, XGBoost
- **Feature Extraction**: TF-IDF, tldextract, urllib
- **Language**: Python 3

---

## 📄 License

This project is for academic/educational purposes.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

<p align="center">
  Built with ❤️ for cybersecurity
</p>
