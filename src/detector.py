
from pathlib import Path
import re
import logging
import joblib
import streamlit as st

try:
    from .features import url_indicators, normalize_url
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.features import url_indicators, normalize_url

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]

URL_MODEL_PATH = ROOT / "models/url_model.joblib"
EMAIL_MODEL_PATH = ROOT / "models/email_model.joblib"

URL_PATTERN = re.compile(
    r"(?i)\b(?:https?://|www\.)[^\s<>\"']+"
)

URGENT = re.compile(
    r"\b(urgent|immediately|act now|suspended)\b",
    re.I
)

CREDENTIALS = re.compile(
    r"\b(password|otp|verify your account|"
    r"login credentials)\b",
    re.I
)


@st.cache_resource
def load_url_model():
    if URL_MODEL_PATH.exists():
        return joblib.load(URL_MODEL_PATH)
    logger.warning("URL model not found at %s — running rule-based only.", URL_MODEL_PATH)
    return None


@st.cache_resource
def load_email_model():
    if EMAIL_MODEL_PATH.exists():
        return joblib.load(EMAIL_MODEL_PATH)
    logger.warning("Email model not found at %s — running rule-based only.", EMAIL_MODEL_PATH)
    return None


def predict_phishing(model, text):
    if model is None:
        return None

    probabilities = model.predict_proba([text])[0]
    classes = list(model.classes_)

    return float(probabilities[classes.index(1)])


def detect_url(url):
    model = load_url_model()
    findings = url_indicators(url)

    probability = predict_phishing(model, url)

    if probability is None:
        verdict = (
            "⚠️ Suspicious / needs review"
            if findings
            else "ℹ️ No obvious lexical red flags (model not loaded)"
        )
    elif probability >= 0.70:
        verdict = "🚨 Likely phishing"
    elif probability <= 0.20 and not findings:
        verdict = "✅ Likely legitimate"
    else:
        verdict = "⚠️ Suspicious / needs review"

    return {
        "verdict": verdict,
        "probability": probability,
        "indicators": findings
    }


def detect_email(email):
    model = load_email_model()

    findings = []

    if URGENT.search(email):
        findings.append("Urgency language detected")

    if CREDENTIALS.search(email):
        findings.append("Credential-related wording detected")

    urls = [
        u.rstrip(".,);]")
        for u in URL_PATTERN.findall(email)
    ][:30]

    if urls:
        findings.append("Email contains URL(s)")

    probability = predict_phishing(model, email)

    if probability is None:
        verdict = (
            "⚠️ Suspicious / needs review"
            if findings
            else "ℹ️ No obvious text red flags (model not loaded)"
        )
    elif probability >= 0.70:
        verdict = "🚨 Likely phishing"
    elif probability <= 0.20 and not findings:
        verdict = "✅ Likely legitimate"
    else:
        verdict = "⚠️ Suspicious / needs review"

    return {
        "verdict": verdict,
        "probability": probability,
        "indicators": findings,
        "urls": urls
    }
