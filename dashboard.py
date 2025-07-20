import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from datetime import datetime, timedelta
from app.scraper import run_scraper
from app.nlp_classifier import classify_article
from app.geo_locator import extract_locations
from app.data_store import DataStore
import json

st.set_page_config(page_title="OSINT Dashboard", layout="wide")
st.title("OSINT Dashboard")

# Initialize data store
data_store = DataStore()

# Scrape and process articles
if st.button("Scrape News"):
    with st.spinner("Scraping articles..."):
        articles = run_scraper()
        for article in articles:
            if article:
                article['category'] = classify_article(article['text'])
                article['locations'] = extract_locations(article['text'])
                data_store.store_article(article)
        st.success(f"Processed {len(articles)} articles!")

# Filters
category = st.selectbox("Filter by Category", ["All", "Terrorism", "Politics", "Other"])
date_range = st.date_input("Date Range", [datetime.now() - timedelta(days=7), datetime.now()])

# Fetch and display articles
date_range = [date_range[0], date_range[1]] if len(date_range) == 2 else None
category = None if category == "All" else category
articles = data_store.fetch_articles(category, date_range)

# Create DataFrame for display
columns = ['id', 'title', 'text', 'date', 'url', 'source', 'category', 'locations']
df = pd.DataFrame(articles, columns=columns)
st.dataframe(df[['title', 'date', 'category', 'source', 'url']])

# Map visualization
m = folium.Map(location=[30.3753, 69.3451], zoom_start=6)
for article in articles:
    locations = json.loads(article[7])  # Parse JSON string
    for loc in locations:
        folium.Marker(
            [float(loc['latitude']), float(loc['longitude'])],
            popup=f"{loc['name']}: {article[1]}",
            tooltip=loc['name']
        ).add_to(m)
folium_static(m)

# Export option
if st.button("Export Articles"):
    df.to_csv("articles.csv", index=False)
    st.success("Exported to articles.csv")
