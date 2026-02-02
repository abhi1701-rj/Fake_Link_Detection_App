import streamlit as st
import joblib
import numpy as np

model = joblib.load("model.pkl")

FEATURE_NAMES = [
    "url_length",
    "count_dots",
    "count_slash",
    "has_https",
    "has_ip",
    "digit_count",
    "special_char_count",
    "suspicious_words",
    "redirect_count",
    "subdomain_count"
]

st.title("Fake Link Detection")

selected_features = st.multiselect(
    "Select features to use",
    FEATURE_NAMES,
    default=FEATURE_NAMES[:8]
)

feature_values = []

for feature in FEATURE_NAMES:
    if feature in selected_features:
        value = st.number_input(f"Enter {feature}", value=0)
        feature_values.append(value)
    else:
        feature_values.append(0)

features = np.array([feature_values])

if st.button("Predict"):
    prediction = model.predict(features)[0]
    st.success(f"Prediction: {prediction}")
