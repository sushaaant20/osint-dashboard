# Configuration for OSINT Dashboard
NEWS_SITES = [
    "https://www.dawn.com",
    "https://tribune.com.pk",
    "https://www.thenews.com.pk",
    "https://nation.com.pk",
    "https://www.pakistantoday.com.pk",
    "https://www.thefrontierpost.com",
    "https://dailytimes.com.pk",
    "https://www.geo.tv",
    "https://arynews.tv",
    "https://www.samaa.tv"
]

# NLP and ML settings
SPACY_MODEL = "en_core_web_sm"
NLTK_DATA = ["punkt", "averaged_perceptron_tagger", "wordnet"]
MODEL_PATH = "model/classifier_model.joblib"
VECTORIZER_PATH = "model/vectorizer.joblib"
