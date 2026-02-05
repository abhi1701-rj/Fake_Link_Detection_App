import streamlit as st
import joblib
import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))

st.title("📊 URL Detection Dashboard")

url = st.text_input("🔗 Enter a URL", placeholder="https://www.google.com")

def extract_features(url):
    return {
        "url_length": len(url),
        "count_dots": url.count("."),
        "count_slash": url.count("/"),
        "has_https": int(url.startswith("https")),
        "has_ip": int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),
        "digit_count": sum(c.isdigit() for c in url),
        "special_char_count": sum(not c.isalnum() for c in url),
        "suspicious_words": int(any(w in url.lower() for w in ["login","verify","secure","bank","update"])),
        "subdomain_count": max(url.count(".") - 1, 0)
    }

if st.button("🔍 Analyze URL"):
    features = extract_features(url)
    df = pd.DataFrame([features])

    prediction = model.predict(df)[0]

    if prediction == 1:
        st.success("✅ This URL looks SAFE")
    else:
        st.error("❌ This URL looks FAKE")

    st.subheader("🔎 Extracted Features")
    st.dataframe(df, width="stretch")

    st.subheader("📈 Feature Visualization")
    st.bar_chart(df.T)
