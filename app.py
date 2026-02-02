import streamlit as st
import joblib
import pandas as pd

# Import feature extraction
from feature_extraction import extract_features

# Page config
st.set_page_config(
    page_title="Fake Link Detection",
    page_icon="🔐",
    layout="centered"
)

st.title("🔍 Fake Link Detection System")
st.write("Enter a URL to check whether it is *Safe* or *Malicious*.")

# Load model (cached for performance)
@st.cache_resource
def load_model():
    return joblib.load("rf_basic.pkl")

model = load_model()

# User input
url = st.text_input("🌐 Enter URL", placeholder="https://example.com")

if st.button("Check URL"):
    if url.strip() == "":
        st.warning("⚠️ Please enter a URL")
    else:
        try:
            # Feature extraction
            features = extract_features(url)

            # Convert to DataFrame (VERY IMPORTANT)
            features_df = pd.DataFrame([features])

            # Prediction
            prediction = model.predict(features_df)[0]

            # Output
            if prediction == 1:
                st.error("🚨 This URL is *MALICIOUS / FAKE*")
            else:
                st.success("✅ This URL is *SAFE*")

        except Exception as e:
            st.error("❌ Error occurred while processing the URL")
            st.code(str(e))