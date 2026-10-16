from functools import lru_cache
from pathlib import Path

import joblib


MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "phishguard_baseline.joblib"
)


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Trained model not found: {MODEL_PATH}"
        )
    return joblib.load(MODEL_PATH)


def analyze_email_text(subject, body):
    email_text = f"Subject: {subject or ''}\nBody: {body or ''}"
    model = load_model()

    prediction = int(model.predict([email_text])[0])
    probabilities = model.predict_proba([email_text])[0]
    classes = list(model.classes_)

    return {
        "predicted_label": prediction,
        "label_0_probability": float(
            probabilities[classes.index(0)]
        ),
        "label_1_probability": float(
            probabilities[classes.index(1)]
        ),
        "note": (
            "Dataset labels include mixed spam, fraud, and phishing "
            "samples. This prediction alone does not confirm phishing."
        ),
    }
