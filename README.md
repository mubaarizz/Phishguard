# 🛡️ PHISHGUARD

### Machine-Learning-Assisted Email Phishing Detection

PHISHGUARD is an email security tool designed to help identify potential phishing indicators in suspicious emails. It combines email parsing, header analysis, URL inspection, and machine-learning-based classification to assist users in evaluating email security risks.

PHISHGUARD offers two interfaces:

- **Terminal Interface (CLI):** Launch PHISHGUARD directly using `./phishguard` or provide an email file path for analysis.
- **Web Interface:** Use a Flask-powered web application to submit emails and review analysis results in your browser.

The project is intended for educational, research, and defensive cybersecurity purposes.

---

## 📌 Table of Contents

1. Features
2. How PHISHGUARD Works
3. Prerequisites
4. Dataset Download and Model Training
5. Project Structure
6. Finding the Project Directory
7. Installation and Setup
8. Python Dependencies
9. Model Verification
10. Using the Terminal Interface
11. Using the Web Interface
12. Choosing Between Interfaces
13. Troubleshooting
14. Security Considerations and Limitations
15. License and Disclaimer

---

## ✨ Features

- Terminal-based email analysis.
- Direct email analysis using a file path.
- Browser-based Flask web interface.
- Email content parsing.
- Email header analysis.
- URL inspection using implemented checks.
- Machine-learning-based email classification.
- Browser-based analysis reports.
- Included pre-trained classification model.
- Local execution on Linux.

## 🔍 How PHISHGUARD Works

1. **Email Input:** Provide an email through the terminal or web interface.
2. **Email Parsing:** Extract relevant email content.
3. **Header Analysis:** Examine available header information for potential warning signs.
4. **URL Analysis:** Inspect URLs using the application's implemented checks.
5. **Machine-Learning Analysis:** Use the pre-trained model to classify email content.
6. **Results:** Display the available analysis results through the selected interface.

PHISHGUARD provides supporting security indicators, not a guarantee that an email is safe or malicious.

---

## 💻 Prerequisites

### Tested Environment

- Kali Linux
- Python 3.14.7
- pip 26.1.2
- Bash
- GNU Nano 9.2 (for editing documentation)

Other Linux distributions and Python versions may work but have not necessarily been tested.

### Required Software

- Python 3
- pip
- Python `venv` module
- `curl`
- `xdg-open` for automatic browser launching
- A modern web browser

Check your installed versions:

```bash
python3 --version
python3 -m pip --version
```

If required system packages are missing, install them on Kali Linux:

```bash
sudo apt update
sudo apt install python3-venv curl
```

---

## Dataset

PHISHGUARD comes with a pre-trained machine learning model that is ready to use for phishing email detection. You do not need to train the model before using the tool.

If you want to train the model yourself, retrain it, or experiment with the training process, you can download the dataset provided below and use it for training.

**Download Dataset:** [Phishguard_Dataset.zip]([https://github.com/mubaarizz/Phishguard/releases/tag/v1.0.0])

The dataset includes:
- Enron
- Ling
- SpamAssassin
- Nigerian Fraud
- CEAS-08
- Nazario
- Combined Email Dataset

**Note:** Training is optional for normal use. The pre-trained model is already included in the repository. Please follow the applicable dataset licences and terms when using or redistributing the data.

---

## 📁 Project Structure

The project directory should contain the following files and folders:

```text
Phishguard/
├── app/
│   ├── core/
│   ├── templates/
│   ├── ui/
│   ├── main.py
│   └── web.py
├── models/
│   └── phishguard_baseline.joblib
├── src/
│   ├── prepare_dataset.py
│   ├── train_baseline.py
│   └── test_baseline.py
├── requirements.txt
├── phishguard
├── start_phishguard
├── start.sh
├── end
└── README.md
```

| File or Directory | Purpose |
|---|---|
| `app/` | Main application code |
| `app/core/` | Email analysis and machine-learning components |
| `app/templates/` | Web interface templates |
| `app/ui/` | Terminal interface components |
| `app/main.py` | CLI entry point |
| `app/web.py` | Flask web application |
| `models/` | Pre-trained model |
| `src/` | Dataset preparation, training, and testing scripts |
| `requirements.txt` | Python dependency list |
| `phishguard` | CLI launcher |
| `start_phishguard` | Web startup script |
| `start.sh` | Alternative web startup script |
| `end` | Web shutdown script |

This is the expected structure. Verify filenames against the actual repository if the project changes.

---

## 📍 Finding the Project Directory

Before installing dependencies or launching PHISHGUARD, navigate to the project directory.

### Method 1: Navigate to the Default Location

If the project is in your home directory:

```bash
cd ~/Phishguard
```

Check your current directory:

```bash
pwd
```

The output should identify your actual PHISHGUARD directory.

### Method 2: Find the Directory

If you are unsure where the project is stored:

```bash
find ~ -type d -name "Phishguard" 2>/dev/null
```

Use the returned path with `cd`.

### Method 3: Verify the Files

```bash
ls -la
```

Confirm that you can see `app/`, `models/`, `requirements.txt`, and the launch scripts.

---

## ⚙️ Installation and Setup

Complete these steps before running either interface.

### Step 1: Navigate to the Project

```bash
cd ~/Phishguard
```

Use your actual project path if it differs.

### Step 2: Create a Virtual Environment

```bash
python3 -m venv .venv
```

The virtual environment keeps the project's Python dependencies separate from other applications.

If `.venv` already exists, you generally do not need to recreate it.

### Step 3: Activate the Environment

```bash
source .venv/bin/activate
```

Your terminal prompt may now display `(.venv)`.

### Step 4: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 5: Install the Required Libraries

```bash
python -m pip install -r requirements.txt
```

Wait for the installation to finish successfully before proceeding.

### Step 6: Check the Dependencies

```bash
python -m pip check
```

This checks for dependency conflicts in the active environment.

### Step 7: Verify the Launch Scripts

```bash
ls -l phishguard start_phishguard start.sh end
```

If a script lacks execute permission, grant it as needed:

```bash
chmod +x phishguard start_phishguard start.sh end
```

---

## 📦 Python Dependencies

PHISHGUARD uses the libraries listed in `requirements.txt`.

| Package | Purpose |
|---|---|
| Flask | Web application framework |
| beautifulsoup4 | HTML parsing |
| joblib | Loading the trained model |
| pandas | Dataset processing |
| pyfiglet | Terminal banner styling |
| rich | Formatted terminal output |
| scikit-learn | Machine-learning functionality |

The exact versions are pinned in `requirements.txt`.

**You do not need to install these packages individually.** The following command installs the listed dependencies:

```bash
python -m pip install -r requirements.txt
```

Run it with the virtual environment activated.

---

## 🧠 Model Verification

PHISHGUARD uses the pre-trained model:

`models/phishguard_baseline.joblib`

Verify that it exists:

```bash
ls -lh models/phishguard_baseline.joblib
```

The model is included in the repository and is required for machine-learning-based classification. The original training dataset is not required for normal use of the existing model.

---

## 🖥️ Using the Terminal Interface (CLI)

Once the installation and model checks are complete, you can use PHISHGUARD from your terminal.

### Method 1: Launch PHISHGUARD Directly

From the project directory, run:

```bash
./phishguard
```

This launches the CLI without an email path argument. Follow the on-screen instructions provided by the application.

### Method 2: Analyze an Email File

```bash
./phishguard /path/to/email.eml
```

Replace `/path/to/email.eml` with the actual path to your email file.

For example, if `sample.eml` is in the current directory:

```bash
./phishguard sample.eml
```

If the email is in your Documents directory:

```bash
./phishguard ~/Documents/sample.eml
```

Only analyze emails you are authorized to access.

---

## 🌐 Using the Web Interface

### Step 1: Start the Application

From the project directory, run:

```bash
./start_phishguard
```

The script checks whether the local server is responding. If it is not, it attempts to start Flask and open your browser.

### Step 2: Open the Application

Visit:

http://127.0.0.1:5000/

If the browser does not open automatically, enter the address manually.

### Step 3: Analyze an Email

Use the web interface to submit an email and review the available analysis results.

### Step 4: Stop the Web Server

```bash
./end
```

### Web Server Logs

If the application fails to start, inspect the log:

```bash
cat /tmp/phishguard-flask.log
```

Check whether the server responds:

```bash
curl -I http://127.0.0.1:5000/
```

The default server is intended for local use. Do not expose it to an untrusted network without reviewing and securing the deployment.

---

## 🔄 Choosing Between the Interfaces

| Feature | Terminal Interface | Web Interface |
|---|---|---|
| Launch command | `./phishguard` | `./start_phishguard` |
| Interaction | Terminal | Browser |
| Email analysis | Supported | Supported |
| Results | Terminal output | Browser-based results |
| Best suited for | Quick command-line analysis | Visual interaction and report viewing |

Both interfaces use the application's analysis components and pre-trained model.

---

## 🧪 Dataset and Model Training

The original training dataset is not included in this repository.

The `src/` directory contains scripts for dataset preparation, training, and testing:

- `src/prepare_dataset.py`
- `src/train_baseline.py`
- `src/test_baseline.py`

Retraining requires the expected dataset files at the locations used by the scripts. Review the scripts before running them and check the dataset's license and redistribution terms before sharing it.

---

## 🛠️ Troubleshooting

### Missing Files or Wrong Directory

```bash
pwd
ls -la
```

Confirm that you are in the correct project directory.

### Permission Denied

```bash
chmod +x phishguard
```

Retry the command after verifying the file exists.

### Missing Python Modules

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Model File Not Found

```bash
ls -lh models/phishguard_baseline.joblib
```

Verify that the model exists and that you are running the application from the correct project directory.

### Web Interface Does Not Open

```bash
curl -I http://127.0.0.1:5000/
cat /tmp/phishguard-flask.log
```

Check the log and confirm that the server started successfully.

### Port 5000 Is Already in Use

Identify the process using the port before stopping anything. Do not terminate unrelated processes.

### Dependency Conflicts

```bash
source .venv/bin/activate
python -m pip check
```

Resolve any reported issues before retrying.

---

## 🔐 Security Considerations and Limitations

- PHISHGUARD provides automated indicators, not a definitive security verdict.
- Machine-learning predictions may produce false positives and false negatives.
- A legitimate classification does not prove that an email is trustworthy.
- URL checks do not necessarily establish whether a website is safe.
- Treat email content, attachments, and URLs as untrusted input.
- Avoid submitting confidential or personal emails to shared or public deployments without assessing the privacy implications.
- Only analyze email files you are authorized to access.
- The default Flask server is intended for local use, not direct public deployment.

## 📄 License

No license has been specified yet. Until a license is added, do not assume the project is licensed for unrestricted reuse, modification, or redistribution.

## ⚠️ Disclaimer

PHISHGUARD is intended for educational, research, and defensive cybersecurity purposes. Its results should be treated as supporting evidence rather than a guarantee of security.

---

**PHISHGUARD | Email Security Through Machine Learning**
