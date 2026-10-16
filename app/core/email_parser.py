from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
from pathlib import Path
from bs4 import BeautifulSoup
from app.core.header_analyzer import analyze_headers
from urllib.parse import urlsplit
import re


URL_PATTERN = re.compile(r'https?://[^\s<>"\'\])}]+', re.IGNORECASE)
def clean_email_text(text):
    text = re.sub(r'\\([\\`*_{}\[\]()#+.!|>-])', r'\1', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)\*(?!\*)', r'\1', text)
    return text

def parse_email(file_path):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Email file not found: {path}")

    with path.open("rb") as email_file:
        message = BytesParser(policy=policy.default).parse(email_file)

    plain_parts = []
    html_parts = []

    if message.is_multipart():
        parts = message.walk()
    else:
        parts = [message]

    for part in parts:
        if part.is_multipart():
            continue

        if part.get_content_disposition() == "attachment":
            continue

        content_type = part.get_content_type()

        if content_type not in ("text/plain", "text/html"):
            continue

        try:
            content = part.get_content()
        except (UnicodeDecodeError, LookupError, ValueError):
            continue

        if not isinstance(content, str):
            continue

        if content_type == "text/plain":
            plain_parts.append(content)
        else:
            html_parts.append(content)

    html_visible_text = []
    html_urls = []

    for html in html_parts:
        soup = BeautifulSoup(html, "html.parser")

        for element in soup(["script", "style", "noscript"]):
            element.decompose()

        html_visible_text.append(soup.get_text(" ", strip=True))

        for tag in soup.find_all(["a", "area"]):
            href = tag.get("href")
            if isinstance(href, str) and href.strip():
                html_urls.append(href.strip())

    plain_body = clean_email_text("\n".join(plain_parts))
    visible_html = clean_email_text("\n".join(html_visible_text))
    body = "\n".join(part for part in (plain_body, visible_html) if part)

    urls = URL_PATTERN.findall(plain_body)
    urls.extend(URL_PATTERN.findall(visible_html))
    urls.extend(html_urls)

    unique_urls = list(dict.fromkeys(urls))

    url_details = []
    for url in unique_urls:
        try:
            parsed_url = urlsplit(url)
            url_details.append({
                "url": url,
                "scheme": parsed_url.scheme,
                "hostname": parsed_url.hostname,
            })
        except ValueError:
            url_details.append({
                "url": url,
                "scheme": "",
                "hostname": None,
            })

    sender_name, sender_address = parseaddr(message.get("From", ""))
    reply_name, reply_address = parseaddr(message.get("Reply-To", ""))

    return {
        "file_name": path.name,
        "subject": str(message.get("Subject", "")),
        "sender_name": sender_name,
        "sender_email": sender_address,
        "reply_to": reply_address,
        "recipient": str(message.get("To", "")),
        "date": str(message.get("Date", "")),
        "plain_body": plain_body,
        "html_visible_text": visible_html,
        "body": body,
        "urls": url_details,
        "header_analysis": analyze_headers(message),
        "headers": {
            "authentication_results": str(message.get("Authentication-Results", "")),
            "received_spf": str(message.get("Received-SPF", "")),
            "dkim_signature_present": bool(message.get("DKIM-Signature")),
        },
    }
