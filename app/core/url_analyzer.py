import ipaddress
import re
from urllib.parse import urlsplit, unquote


SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd",
    "cutt.ly", "rb.gy", "ow.ly", "shorturl.at",
}

SUSPICIOUS_WORDS = {
    "login", "verify", "account", "password",
    "secure", "update", "signin", "confirm",
}


def analyze_url(url):
    findings = []
    score = 0

    try:
        parsed = urlsplit(url.strip())
        hostname = parsed.hostname
    except (ValueError, AttributeError):
        return {
            "url": url,
            "hostname": None,
            "risk_score": 0,
            "risk_level": "Unknown",
            "findings": ["URL could not be parsed safely"],
        }

    if parsed.scheme not in ("http", "https"):
        findings.append("URL does not use HTTP or HTTPS")
        score += 1

    if not hostname:
        findings.append("Hostname is missing or invalid")
        score += 3
    else:
        hostname = hostname.lower().rstrip(".")

        try:
            ipaddress.ip_address(hostname)
            findings.append("URL uses an IP address instead of a domain name")
            score += 2
        except ValueError:
            pass

        if hostname in SHORTENER_DOMAINS:
            findings.append("Known URL-shortener domain")
            score += 1

        if hostname.startswith("xn--") or ".xn--" in hostname:
            findings.append("Internationalized/punycode hostname")
            score += 2

        if hostname.count(".") >= 4:
            findings.append("Hostname has an unusually high number of subdomains")
            score += 1

        if len(hostname) > 60:
            findings.append("Unusually long hostname")
            score += 1

    if parsed.username is not None or parsed.password is not None:
        findings.append("URL contains user-information before the hostname")
        score += 2

    decoded_url = unquote(url).lower()

    if "@" in urlsplit(url).netloc:
        findings.append("URL authority contains @, which can obscure the destination")
        score += 2

    if re.search(r"%[0-9a-fA-F]{2}", url):
        findings.append("URL contains percent-encoded characters")
        score += 1

    if parsed.scheme == "http":
        findings.append("Connection scheme is HTTP, not HTTPS")
        score += 1

    matched_words = sorted(
        word for word in SUSPICIOUS_WORDS
        if word in decoded_url
    )

    if matched_words:
        findings.append(
            "Account-related keywords in URL: " + ", ".join(matched_words)
        )
        score += 1

    if len(url) > 200:
        findings.append("Unusually long URL")
        score += 1

    if not findings:
        findings.append("No configured URL risk indicators detected")

    if score >= 5:
        risk_level = "High"
    elif score >= 3:
        risk_level = "Medium"
    elif score >= 1:
        risk_level = "Low"
    else:
        risk_level = "No indicators"

    return {
        "url": url,
        "hostname": hostname,
        "risk_score": score,
        "risk_level": risk_level,
        "findings": findings,
    }


if __name__ == "__main__":
    test_urls = [
        "https://example.com",
        "http://192.0.2.10/login",
        "https://example.com@evil.example/login",
    ]

    for test_url in test_urls:
        result = analyze_url(test_url)
        print(f"\nURL: {result['url']}")
        print(f"Risk level: {result['risk_level']}")
        print(f"Indicators: {'; '.join(result['findings'])}")
