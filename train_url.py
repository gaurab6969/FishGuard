
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


# CSV columns: URL, label
# label: 1 = phishing, 0 = legitimate

df = pd.read_csv("data/processed/urls.csv")

df = df[["URL", "label"]].dropna()
df = df.rename(columns={"URL": "url"})
df["url"] = df["url"].astype(str).str.strip()
df["label"] = pd.to_numeric(df["label"], errors="coerce")

df = df[df["label"].isin([0, 1])]
df = df[df["url"] != ""]
df = df.drop_duplicates("url")

X_train, X_test, y_train, y_test = train_test_split(
    df["url"],
    df["label"].astype(int),
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        analyzer="char",
        ngram_range=(3, 5),
        min_df=2,
        max_features=300000
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

joblib.dump(model, "models/url_model.joblib")

print("URL model saved.")
