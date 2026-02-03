import streamlit as st
import pandas as pd
import joblib
import os

# ---------------- Page config ----------------
st.set_page_config(page_title="Fake Link Detection", layout="wide")

# ---------------- Load model ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(MODEL_PATH)

# ---------------- Header ----------------
st.title("🚨 Fake Link Detection System")
st.write("Check whether a URL is **SAFE or FAKE** using Machine Learning")
st.divider()

# ---------------- Input ----------------
url = st.text_input("Enter a URL to test")

if st.button("Check URL"):
    if url.strip() == "":
        st.warning("Please enter a URL")
    else:
        # -------- Feature extraction --------
        url_length = len(url)
        count_dots = url.count(".")
        count_slash = url.count("/")
        has_https = 1 if url.startswith("https://") else 0
        has_ip = 1 if any(part.isdigit() for part in url.replace("http://","").replace("https://","").split(".")[:4]) else 0
        digit_count = sum(c.isdigit() for c in url)
        special_char_count = sum(not c.isalnum() for c in url)
        suspicious_words = sum(word in url.lower() for word in ["login", "secure", "verify", "update"])
        subdomain_count = max(url.count(".") - 1, 0)

        # -------- Create DataFrame --------
        features = pd.DataFrame([[
            url_length,
            count_dots,
            count_slash,
            has_https,
            has_ip,
            digit_count,
            special_char_count,
            suspicious_words,
            subdomain_count
        ]], columns=[
            "url_length",
            "count_dots",
            "count_slash",
            "has_https",
            "has_ip",
            "digit_count",
            "special_char_count",
            "suspicious_words",
            "subdomain_count"
        ])

        # -------- Prediction --------
        prediction = model.predict(features)[0]

        if prediction == 1:
            st.success("✅ This URL looks SAFE")
        else:
            st.error("❌ This URL looks FAKE")

        # -------- Show features --------
        st.subheader("Extracted Features")
        st.dataframe(features)

        # -------- Simple chart (NO plotly) --------
        st.subheader("Feature Visualization")
        chart_df = features.T
        chart_df.columns = ["Value"]
        st.bar_chart(chart_df)

# ---------------- Footer ----------------
st.divider()
st.caption("© Fake Link Detection | Developed by Abhishek Reddy")
