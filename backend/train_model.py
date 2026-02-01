import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extraction import extract_features

print("🔹 Loading dataset...")

df = pd.read_csv("../data/urls.csv")
print("🔹 Dataset loaded")
print(df.head())

print("🔹 Extracting features...")
X = df["url"].apply(extract_features).tolist()
y = df["label"]

print("🔹 Feature extraction done")
print("Total samples:", len(X))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("🔹 Training model...")

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "model.pkl")

print("✅ Model trained and saved as model.pkl")
