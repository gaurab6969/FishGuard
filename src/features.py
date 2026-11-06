
from urllib.parse import urlsplit, unquote
import ipaddress
import re

SUSPICIOUS_WORDS = {
    "login", "verify", "secure", "account",
    "password", "signin", "update", "payment",
    "recover", "confirm", "wallet"
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co",
    "is.gd", "cutt.ly", "rb.gy"
}


def normalize_url(raw):
    raw = (raw or "").strip()

    if not raw:
        return ""

    if "://" not in raw:
        raw = "http://" + raw

    return raw


def url_features(raw):
    parsed = urlsplit(normalize_url(raw))
    host = (parsed.hostname or "").lower().rstrip(".")

    path = unquote(parsed.path + "?" + parsed.query)

    try:
        ipaddress.ip_address(host.strip("[]"))
        is_ip = 1
    except ValueError:
        is_ip = 0

    tokens = set(
        re.findall(
            r"[a-zA-Z]{3,}",
            (host + " " + path).lower()
        )
    )

    return {
        "length": len(raw),
        "host_length": len(host),
        "dots": host.count("."),
        "hyphens": raw.count("-"),
        "at_symbols": raw.count("@"),
        "digit_ratio": sum(c.isdigit() for c in raw)
                       / max(1, len(raw)),
        "https": int(parsed.scheme == "https"),
        "ip_host": is_ip,
        "punycode": int("xn--" in host),
        "encoded": int("%" in raw),
        "shortener": int(host in SHORTENERS),
        "suspicious_word": int(
            bool(tokens & SUSPICIOUS_WORDS)
        )
    }


def url_indicators(raw):
    f = url_features(raw)
    findings = []

    if f["ip_host"]:
        findings.append("IP address used as hostname")

    if f["at_symbols"]:
        findings.append("Contains @ character")

    if f["punycode"]:
        findings.append("Punycode hostname")

    if f["shortener"]:
        findings.append("URL shortener detected")

    if f["length"] > 100:
        findings.append("Unusually long URL")

    if f["suspicious_word"]:
        findings.append("Account or credential-related wording")

    if not f["https"]:
        findings.append("HTTPS not used")

    return findings
