import pytest
from unittest.mock import patch, MagicMock
from src.detector import detect_url, detect_email, predict_phishing


class TestPredictPhishing:
    def test_returns_none_when_model_is_none(self):
        assert predict_phishing(None, "test") is None

    def test_returns_probability(self):
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.2, 0.8]]
        mock_model.classes_ = [0, 1]

        prob = predict_phishing(mock_model, "test phishing text")
        assert prob == pytest.approx(0.8)

    def test_handles_reversed_class_order(self):
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.7, 0.3]]
        mock_model.classes_ = [1, 0]

        prob = predict_phishing(mock_model, "test")
        # class 1 is at index 0, probability 0.7
        assert prob == pytest.approx(0.7)


class TestDetectUrlWithoutModel:
    @patch("src.detector.load_url_model", return_value=None)
    def test_suspicious_url_without_model(self, _):
        result = detect_url("http://192.168.1.1/login")
        assert result["probability"] is None
        assert "Suspicious" in result["verdict"]
        assert len(result["indicators"]) > 0

    @patch("src.detector.load_url_model", return_value=None)
    def test_clean_url_without_model(self, _):
        result = detect_url("https://google.com")
        assert result["probability"] is None
        assert "model not loaded" in result["verdict"]
        assert len(result["indicators"]) == 0


class TestDetectEmailWithoutModel:
    @patch("src.detector.load_email_model", return_value=None)
    def test_urgent_email(self, _):
        result = detect_email("URGENT: Act now or your account will be suspended!")
        assert result["probability"] is None
        assert "Suspicious" in result["verdict"]
        assert "Urgency language detected" in result["indicators"]

    @patch("src.detector.load_email_model", return_value=None)
    def test_credential_email(self, _):
        result = detect_email("Please enter your password to verify your account.")
        assert "Credential-related wording detected" in result["indicators"]

    @patch("src.detector.load_email_model", return_value=None)
    def test_email_with_urls(self, _):
        result = detect_email("Click here: https://evil.com/steal")
        assert "Email contains URL(s)" in result["indicators"]
        assert "https://evil.com/steal" in result["urls"]

    @patch("src.detector.load_email_model", return_value=None)
    def test_clean_email(self, _):
        result = detect_email("Hello, how are you doing today?")
        assert result["probability"] is None
        assert "model not loaded" in result["verdict"]
        assert len(result["indicators"]) == 0
        assert len(result["urls"]) == 0
