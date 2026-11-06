import pytest
from src.features import normalize_url, url_features, url_indicators


class TestNormalizeUrl:
    def test_empty_string(self):
        assert normalize_url("") == ""

    def test_none(self):
        assert normalize_url(None) == ""

    def test_adds_http_if_missing(self):
        assert normalize_url("example.com") == "http://example.com"

    def test_preserves_https(self):
        assert normalize_url("https://example.com") == "https://example.com"

    def test_strips_whitespace(self):
        assert normalize_url("  http://example.com  ") == "http://example.com"


class TestUrlFeatures:
    def test_basic_url(self):
        f = url_features("https://example.com")
        assert f["https"] == 1
        assert f["ip_host"] == 0
        assert f["shortener"] == 0

    def test_ip_host(self):
        f = url_features("http://192.168.1.1/login")
        assert f["ip_host"] == 1

    def test_shortener(self):
        f = url_features("http://bit.ly/abc123")
        assert f["shortener"] == 1

    def test_punycode(self):
        f = url_features("http://xn--e1afmapc.xn--p1ai/")
        assert f["punycode"] == 1

    def test_at_symbol(self):
        f = url_features("http://legitimate.com@evil.com")
        assert f["at_symbols"] >= 1

    def test_suspicious_word(self):
        f = url_features("http://evil.com/login/verify")
        assert f["suspicious_word"] == 1

    def test_no_https(self):
        f = url_features("http://example.com")
        assert f["https"] == 0

    def test_digit_ratio(self):
        f = url_features("http://123456789.com")
        assert f["digit_ratio"] > 0


class TestUrlIndicators:
    def test_ip_host_indicator(self):
        indicators = url_indicators("http://192.168.1.1/page")
        assert "IP address used as hostname" in indicators

    def test_shortener_indicator(self):
        indicators = url_indicators("http://bit.ly/abc")
        assert "URL shortener detected" in indicators

    def test_at_symbol_indicator(self):
        indicators = url_indicators("http://good.com@evil.com")
        assert "Contains @ character" in indicators

    def test_punycode_indicator(self):
        indicators = url_indicators("http://xn--e1afmapc.xn--p1ai/")
        assert "Punycode hostname" in indicators

    def test_long_url_indicator(self):
        long = "https://example.com/" + "a" * 200
        indicators = url_indicators(long)
        assert "Unusually long URL" in indicators

    def test_no_https_indicator(self):
        indicators = url_indicators("http://example.com")
        assert "HTTPS not used" in indicators

    def test_https_no_flag(self):
        indicators = url_indicators("https://example.com")
        assert "HTTPS not used" not in indicators

    def test_clean_url_minimal_indicators(self):
        indicators = url_indicators("https://google.com")
        assert len(indicators) == 0
