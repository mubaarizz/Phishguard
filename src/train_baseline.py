from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
)

DATA = Path("dataset/processed/combined_emails.csv")
MODEL_DIR = Path("models")
REPORT_DIR = Path("reports")

MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA)

df = df.dropna(subset=["text", "label"]).copy()
df["text"] = df["text"].astype(str).str.strip()
df = df[df["text"] != ""]
df["label"] = df["label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.20,
    random_state=42,
    stratify=df["label"],
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=2,
        max_features=50000,
        sublinear_tf=True,
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        random_state=42,
    )),
])

print(f"Total emails: {len(df)}")
print(f"Training emails: {len(X_train)}")
print(f"Testing emails: {len(X_test)}")
print("\nTraining baseline model...")

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, predictions), 4))
print("\nClassification report:")
report = classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Label 0", "Label 1"],
    zero_division=0,
)
print(report)

print("Confusion matrix (rows=actual, columns=predicted):")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))

model_path = MODEL_DIR / "phishguard_baseline.joblib"
joblib.dump(model, model_path)

report_path = REPORT_DIR / "baseline_evaluation.txt"
with report_path.open("w", encoding="utf-8") as f:
    f.write(f"Dataset: {DATA}\n")
    f.write(f"Total emails: {len(df)}\n")
    f.write(f"Training emails: {len(X_train)}\n")
    f.write(f"Testing emails: {len(X_test)}\n")
    f.write(f"Accuracy: {accuracy_score(y_test, predictions):.4f}\n\n")
    f.write(report)
    f.write("\nConfusion matrix (rows=actual, columns=predicted):\n")
    f.write(str(confusion_matrix(y_test, predictions, labels=[0, 1])))
    f.write("\n\nCaution: source dataset labels mix spam, fraud, and phishing.")
    f.write("\nThis is a baseline text classifier, not proof of phishing.")

print(f"\nModel saved: {model_path}")
print(f"Evaluation saved: {report_path}")
print("Note: label 1 is the dataset's original positive label, not verified phishing.")
