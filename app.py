import streamlit as st
import numpy as np
import os
import joblib
import re
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(MODEL_PATH)

def extract_features(url):
    features = {}
    features["url_length"] = len(url)
    features["count_dots"] = url.count(".")
    features["count_slash"] = url.count("/")
    features["has_https"] = 1 if url.startswith("https") else 0
    features["has_ip"] = 1 if re.search(r'\b\d{1,3}(\.\d{1,3}){3}\b', url) else 0
    features["digit_count"] = sum(c.isdigit() for c in url)
    features["special_char_count"] = len(re.findall(r'[^\w]', url))
    suspicious = ["login", "verify", "secure", "account", "update"]
    features["suspicious_words"] = sum(w in url.lower() for w in suspicious)
    parsed = urlparse(url)
    features["subdomain_count"] = parsed.netloc.count('.') - 1
    return features

st.title("Fake Link Detection")

url = st.text_input("Enter a URL to test")

if url:
    extracted = extract_features(url)
    features = np.array([[ 
        extracted["url_length"],
        extracted["count_dots"],
        extracted["count_slash"],
        extracted["has_https"],
        extracted["has_ip"],
        extracted["digit_count"],
        extracted["special_char_count"],
        extracted["suspicious_words"],
        extracted["subdomain_count"]
    ]])

    st.write("Extracted features:", extracted)

    if st.button("Check URL"):
        prediction = model.predict(features)[0]
        if prediction == 1:
            st.success("✅ This URL looks SAFE")
        else:
            st.error("🚨 This URL looks FAKE")
