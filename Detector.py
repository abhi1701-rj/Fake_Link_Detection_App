import streamlit as st
import joblib
import urllib.parse
from rules import rule_based_check
from whois_check import get_domain_age

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# Load ML model and vectorizer
@st.cache_resource
def load_ml():
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_ml()

# Page config
st.set_page_config(
    page_title="Fake Link Detection System",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 Fake Link Detection System")
st.write("Hybrid Detection: Rule-based + Machine Learning")

# Input
url = st.text_input("🔗 Enter a URL to analyze", "https://www.google.com")

# Final decision logic
def final_decision(url, ml_conf):
    reasons = rule_based_check(url)

    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.replace("www.", "")

    age = get_domain_age(domain)

    if age != -1 and age < 180:
        reasons.append("Newly registered domain")

    if len(reasons) >= 2:
        return "FAKE ❌", reasons, age

    if ml_conf < 0.7:
        return "SUSPICIOUS ⚠️", reasons, age

    return "SAFE ✅", reasons, age

# Analyze button
if st.button("🔍 Analyze URL"):

    if not url.startswith(("http://", "https://")):
        st.error("Please enter a valid URL starting with http or https")
    else:
        # ML Prediction
        vector = vectorizer.transform([url])
        prediction = model.predict(vector)[0]

        try:
            confidence = max(model.predict_proba(vector)[0])
        except:
            confidence = 0.5

        # Final result
        result, reasons, age = final_decision(url, confidence)

        # Display
        st.subheader(f"Result: {result}")
        st.write(f"🔐 ML Confidence: **{confidence:.2f}**")

        if age != -1:
            st.write(f"📅 Domain Age: **{age} days**")

        if reasons:
            st.warning("⚠️ Risk Factors Detected:")
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.success("No suspicious patterns detected")

st.markdown("---")
st.caption("© Fake Link Detection | Developed by Abhishek Reddy")
