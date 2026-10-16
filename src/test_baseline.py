from pathlib import Path
import joblib

model_path = Path("models/phishguard_baseline.joblib")
model = joblib.load(model_path)

email_text = """Subject: Urgent: Verify your account
Body: Your account will be suspended. Click here to verify your password immediately."""

prediction = model.predict([email_text])[0]
probabilities = model.predict_proba([email_text])[0]

print("\n=== PHISHGUARD ML TEST ===")
print("Predicted dataset label:", prediction)
print(f"Label 0 probability: {probabilities[0]:.2%}")
print(f"Label 1 probability: {probabilities[1]:.2%}")
print("\nNote: Labels represent the training dataset classes,")
print("not verified phishing classifications.")
