import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

# Page config
st.set_page_config(page_title="Fake Link Detection", layout="wide")

# Load ML model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(MODEL_PATH)

# Header
st.markdown("<h1 style='text-align:center;color:#1f77b4;'>🚨 Fake Link Detection Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Tabs for Test URL and Dashboard
tab1, tab2 = st.tabs(["Test URL", "Dashboard"])

# ----- Tab 1: Test URL -----
with tab1:
    st.header("Check a URL")
    url = st.text_input("Enter a URL to test")
    
    if st.button("Check URL"):
        if url:
            # Feature extraction
            url_length = len(url)
            count_dots = url.count(".")
            count_slash = url.count("/")
            has_https = 1 if "https://" in url else 0
            has_ip = 1 if any(char.isdigit() for char in url.split("//")[-1].split("/")[0].split(".")) else 0
            digit_count = sum(c.isdigit() for c in url)
            special_char_count = sum(not c.isalnum() for c in url)
            suspicious_words = sum(word in url.lower() for word in ["login","secure","update","verify"])
            subdomain_count = url.count(".") - 1  # rough estimate
            
            # Feature DataFrame
            features = pd.DataFrame([[
                url_length, count_dots, count_slash, has_https,
                has_ip, digit_count, special_char_count,
                suspicious_words, subdomain_count
            ]], columns=[
                "url_length","count_dots","count_slash","has_https",
                "has_ip","digit_count","special_char_count",
                "suspicious_words","subdomain_count"
            ])
            
            # Prediction
            prediction = model.predict(features)[0]
            st.success(f"Prediction: {'SAFE ✅' if prediction==0 else 'FAKE ❌'}")
            
            # Show extracted features
            st.subheader("Extracted Features")
            st.json({
                "url_length": url_length,
                "count_dots": count_dots,
                "count_slash": count_slash,
                "has_https": has_https,
                "has_ip": has_ip,
                "digit_count": digit_count,
                "special_char_count": special_char_count,
                "suspicious_words": suspicious_words,
                "subdomain_count": subdomain_count
            })

# ----- Tab 2: Dashboard -----
with tab2:
    st.header("Feature Visualization")
    
    # Example dummy stats for demonstration
    example_data = pd.DataFrame({
        "Feature": ["url_length", "count_dots", "count_slash", "digit_count", "special_char_count"],
        "Value": [22, 2, 3, 0, 5]
    })
    fig = px.bar(example_data, x="Feature", y="Value", title="Example Feature Values")
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics example
    col1, col2, col3 = st.columns(3)
    col1.metric("Total URLs Checked", "50")
    col2.metric("Safe URLs", "42")
    col3.metric("Fake URLs", "8")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>© 2026 Fake Link Detection | Developed by Abhishek Reddy</p>", unsafe_allow_html=True)
