
# 🛡️ FishGuard
### Intelligent Phishing URL & Email Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange" />
  <img src="https://img.shields.io/badge/Interface-Streamlit-red?logo=streamlit" />
  <img src="https://img.shields.io/badge/Domain-Cybersecurity-darkgreen" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

---

## 📌 Overview

**FishGuard** is a machine learning-based cybersecurity application designed to identify and detect potential phishing attacks through URL analysis and email content classification.

The system leverages Natural Language Processing (NLP), TF-IDF vectorization, and Logistic Regression to classify suspicious URLs and email messages based on learned patterns.

FishGuard aims to provide an accessible and efficient approach to phishing detection by combining automated threat classification with a user-friendly Streamlit interface.

---

## 🎯 Key Features

- **Phishing URL Detection** – Analyzes URLs and identifies potentially malicious links.
- **Email Phishing Detection** – Classifies email content as legitimate or phishing.
- **Machine Learning Classification** – Uses Logistic Regression for predictive classification.
- **TF-IDF Vectorization** – Converts textual data into numerical features for machine learning.
- **Risk Assessment** – Provides classification results and risk indicators.
- **Interactive Dashboard** – Streamlit-based graphical user interface.
- **Automated Analysis** – Processes user input and generates detection results.

---

## 🧠 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Scikit-learn | Machine learning algorithms |
| TF-IDF | Text feature extraction |
| Logistic Regression | Classification model |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Streamlit | Web-based interface |
| Pickle / Joblib | Model serialization (if implemented) |

---

## 🏗️ System Architecture

```text
                USER INPUT
                    |
          +---------+---------+
          |                   |
       URL INPUT          EMAIL INPUT
          |                   |
          v                   v
     URL ANALYSIS        TEXT PROCESSING
          |                   |
          v                   v
     FEATURE EXTRACTION / TF-IDF
          |                   |
          +---------+---------+
                    |
                    v
             ML CLASSIFIER
          (Logistic Regression)
                    |
                    v
            THREAT CLASSIFICATION
                    |
          +---------+---------+
          |                   |
          v                   v
      LEGITIMATE           PHISHING
          |                   |
          +---------+---------+
                    |
                    v
             RISK ASSESSMENT
                    |
                    v
             STREAMLIT UI
                    |
                    v
             DISPLAY RESULTS
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/FishGuard.git
```

### 2. Navigate to Project Directory

```bash
cd FishGuard
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the FishGuard dashboard.

---

## 📂 Project Structure

```text
FishGuard/
│
├── app.py
│
├── models/
│   ├── phishing_model.pkl
│   └── vectorizer.pkl
│
├── dataset/
│   ├── phishing_urls.csv
│   └── phishing_emails.csv
│
├── modules/
│   ├── url_detector.py
│   ├── email_detector.py
│   └── risk_assessment.py
│
├── utils/
│   ├── preprocessing.py
│   └── feature_extraction.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

*Note: The directory structure is a suggested documentation layout. Adjust it to match the actual implementation.*

---

## 🔬 Machine Learning Methodology

### 1. Data Preprocessing
- Cleaning input text.
- Removing unnecessary characters.
- Normalizing textual data.
- Preparing data for feature extraction.

### 2. Feature Extraction

TF-IDF (Term Frequency–Inverse Document Frequency) transforms textual information into numerical feature vectors.

### 3. Model Training

Logistic Regression is used to learn patterns associated with phishing and legitimate content.

### 4. Prediction

The trained model analyzes input data and predicts its classification.

### 5. Risk Assessment

The system presents the classification result to help users identify potentially suspicious content.

---

## 📊 Performance Evaluation

The following metrics can be used to evaluate the trained model:

| Metric | Description |
|---|---|
| Accuracy | Overall prediction correctness |
| Precision | Correct phishing predictions |
| Recall | Ability to identify phishing samples |
| F1-Score | Balance between precision and recall |
| Confusion Matrix | Classification performance breakdown |

*Add actual evaluation results after measuring model performance on a separate test dataset.*

---

## 🔐 Cybersecurity Applications

FishGuard demonstrates practical applications of machine learning in cybersecurity, including:

- Phishing attack identification.
- Suspicious URL classification.
- Email threat analysis.
- Automated security awareness.
- Machine learning-assisted threat detection.

---

## 🚀 Future Enhancements

- [ ] Real-time URL reputation checking.
- [ ] Domain and DNS-based analysis.
- [ ] SSL certificate validation.
- [ ] WHOIS domain intelligence.
- [ ] Advanced URL feature engineering.
- [ ] Random Forest and XGBoost model comparison.
- [ ] Explainable AI (SHAP).
- [ ] Threat intelligence API integration.
- [ ] REST API deployment using FastAPI.
- [ ] Docker containerization.
- [ ] Cloud deployment.

---

## ⚠️ Disclaimer

FishGuard is an educational cybersecurity project developed for research, learning, and phishing detection demonstrations.

Detection results are predictions and should not be considered a guarantee that a URL or email is safe or malicious.

Always verify suspicious links and messages using additional security tools and trusted threat intelligence sources.

---

## 👨‍💻 Author

**Developed as a Cybersecurity & Machine Learning Project**

**Project:** FishGuard – Phishing URL & Email Detection System

**Domain:** Cybersecurity | Machine Learning | NLP

**Language:** Python

---

## 📜 License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---

<p align="center">
  <b>FishGuard — Detect. Analyze. Protect.</b>
  <br>
  Building smarter defenses against phishing threats.
</p>
