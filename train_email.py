
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# CSV columns: (index), Email Text, Email Type
# Email Type: "Phishing Email" = 1, "Safe Email" = 0

df = pd.read_csv("data/processed/emails.csv")

df = df.rename(columns={"Email Text": "text", "Email Type": "label"})
df = df[["text", "label"]].dropna()
df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].map({
    "Phishing Email": 1, "phishing email": 1,
    "Safe Email": 0, "safe email": 0
})
df["label"] = pd.to_numeric(df["label"], errors="coerce")

df = df[df["label"].isin([0, 1])]
df = df[df["text"] != ""]
df = df.drop_duplicates("text")

X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label"].astype(int),
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_features=250000,
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(classification_report(
    y_test,
    predictions,
    target_names=["Legitimate", "Phishing"]
))

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/email_model.joblib")

print("Email model saved.")
