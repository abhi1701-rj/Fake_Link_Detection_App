import streamlit as st
import joblib
import os
import re
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fake Link Detection",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))

# ---------------- TITLE ----------------
st.title("🚨 Fake Link Detection System")
<<<<<<< HEAD
st.markdown("Detect malicious URLs instantly using **Machine Learning**")
=======
st.write("Check whether a URL is **SAFE or FAKE** using Machine Learning")
st.divider()
>>>>>>> f3ee6fe7d45f3cc6754bc9413aa6c26c78b959d0

st.markdown("---")

# ---------------- INPUT ----------------
url = st.text_input("🔗 Enter a URL to test", placeholder="https://www.google.com")

# ---------------- FEATURE EXTRACTION ----------------
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

# ---------------- PREDICTION ----------------
if st.button("🔍 Analyze URL"):
    if url.strip() == "":
        st.warning("⚠️ Please enter a URL")
    else:
        features_dict = extract_features(url)
        features_df = pd.DataFrame([features_dict])

        prediction = model.predict(features_df)[0]

        # -------- RESULT --------
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 Prediction Result")
            if prediction == 1:
                st.success("✅ This URL looks SAFE")
            else:
                st.error("❌ This URL looks FAKE")

        with col2:
            st.subheader("📊 Key Metrics")
            st.metric("URL Length", features_dict["url_length"])
            st.metric("Dots Count", features_dict["count_dots"])
            st.metric("Special Characters", features_dict["special_char_count"])

        st.markdown("---")

        # -------- FEATURES TABLE --------
        st.subheader("🔎 Extracted Features")
        st.dataframe(features_df, width="stretch")


        # -------- DASHBOARD CHART --------
        st.subheader("📈 Feature Visualization")
        chart_df = pd.DataFrame({
            "Feature": features_dict.keys(),
            "Value": features_dict.values()
        })
        st.bar_chart(chart_df.set_index("Feature"))

st.markdown("---")
st.caption("© Fake Link Detection | Developed by Abhishek Reddy")
