from pathlib import Path
import pandas as pd

RAW_DIR = Path("dataset/raw")
OUT_DIR = Path("dataset/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

frames = []

for path in sorted(RAW_DIR.glob("*.csv")):
    df = pd.read_csv(path)

    required = {"subject", "body", "label"}
    missing = required - set(df.columns)
    if missing:
        print(f"Skipping {path.name}: missing columns {sorted(missing)}")
        continue

    df = df.copy()
    df["source"] = path.stem
    df["subject"] = df["subject"].fillna("").astype(str).str.strip()
    df["body"] = df["body"].fillna("").astype(str).str.strip()

    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["label"])
    df = df[df["subject"].ne("") | df["body"].ne("")]

    df["label"] = df["label"].astype(int)
    df["text"] = (
        "Subject: " + df["subject"] + "\n"
        + "Body: " + df["body"]
    ).str.strip()

    frames.append(df)
    print(
        f"{path.name}: loaded={before}, "
        f"retained={len(df)}, removed={before - len(df)}"
    )

if not frames:
    raise SystemExit("ERROR: No usable CSV datasets found.")

combined = pd.concat(frames, ignore_index=True, sort=False)
output = OUT_DIR / "combined_emails.csv"
combined.to_csv(output, index=False)

print("\nDataset preparation complete.")
print(f"Output: {output}")
print(f"Total emails: {len(combined)}")
print("\nRows by source:")
print(combined["source"].value_counts().to_string())
print("\nOriginal label counts by source:")
print(
    combined.groupby(["source", "label"])
    .size()
    .unstack(fill_value=0)
    .to_string()
)
