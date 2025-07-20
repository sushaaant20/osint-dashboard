import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from joblib import dump, load
from app.config import SPACY_MODEL, MODEL_PATH, VECTORIZER_PATH
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nlp = spacy.load(SPACY_MODEL)

def preprocess_text(text):
    doc = nlp(text.lower())
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def train_classifier():
    try:
        data = pd.read_csv('train_data.csv')  # Expected columns: text, label
        X = data['text'].apply(preprocess_text)
        y = data['label']
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000)),
            ('clf', LogisticRegression())
        ])
        pipeline.fit(X, y)
        os.makedirs('model', exist_ok=True)
        dump(pipeline.named_steps['tfidf'], VECTORIZER_PATH)
        dump(pipeline.named_steps['clf'], MODEL_PATH)
        logger.info("Model trained and saved")
    except Exception as e:
        logger.error(f"Error training classifier: {e}")

def classify_article(text):
    try:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            logger.warning("Model not found, training new model")
            train_classifier()
        vectorizer = load(VECTORIZER_PATH)
        clf = load(MODEL_PATH)
        processed_text = preprocess_text(text)
        vectorized_text = vectorizer.transform([processed_text])
        return clf.predict(vectorized_text)[0]
    except Exception as e:
        logger.error(f"Error classifying text: {e}")
        return "Other"
