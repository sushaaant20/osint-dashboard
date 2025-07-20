OSINT Dashboard
An advanced OSINT dashboard for scraping, classifying, and visualizing news articles from Pakistan-based sites using machine learning and concurrent processing.
Features

Scrapes articles from 10 Pakistan-based news sites using aiohttp and newspaper3k.
Classifies articles (Terrorism, Politics, Other) with a scikit-learn logistic regression model.
Extracts and geocodes locations using spaCy and geopy, with caching in SQLite.
Stores data in SQLite (osint.db).
Visualizes articles with Streamlit and Folium, including category/date filters and a map.

Setup on Fedora Linux

Clone the repository:git clone https://github.com/yourusername/osint-dashboard.git
cd osint-dashboard


Set up a virtual environment:python3 -m venv venv
source venv/bin/activate


Install dependencies:sudo dnf install python3 python3-pip sqlite -y
pip install -r requirements.txt
python3 -m nltk.downloader punkt
python3 -m spacy download en_core_web_sm


Train the ML model:python -c "from app.nlp_classifier import train_classifier; train_classifier()"


Run the dashboard:streamlit run dashboard.py



Project Structure
osint-dashboard/
├── app/
│   ├── config.py           # Configuration
│   ├── scraper.py          # Concurrent scraping
│   ├── nlp_classifier.py   # ML classification
│   ├── geo_locator.py      # Location extraction
│   ├── data_store.py       # SQLite storage
├── dashboard.py            # Streamlit app
├── train_data.csv         # ML training data
├── requirements.txt        # Dependencies
├── .gitignore             # Ignores
└── README.md              # Documentation

Usage

Open http://localhost:8501 in your browser.
Click "Scrape News" to fetch and process articles.
Use filters to view articles by category or date range.
Export articles to CSV with the "Export Articles" button.

Notes

Expand train_data.csv with more labeled articles for better ML accuracy.
Respect news sites’ terms by limiting scraping frequency.
Cache geocoding results to reduce geopy API calls.

