# backend/app/nysc_service.py
"""
NYSC verification scraper.
Drop this file into backend/app/ alongside your other service modules.
Before using, inspect the live NYSC verify page and set:
  - NYSC_VERIFY_URL: the form action URL (or page URL if action is same)
  - FORM_FIELD_CALLUP / FORM_FIELD_CERT_NO / FORM_FIELD_DOB: exact input names.
"""

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry
import logging
from flask import jsonify
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DUMMY_NYSC = {
    "name": "Bashir Mustapha",
    "dob": "2002-02-26",
    "callup_no": "NYSC2025ABC123",
    "certificate_no": "CERT123456",
    "status": "Verified ✅ (dummy)",
}

def verify_nysc_dummy(callup_no=None, certificate_no=None, dob=None):
    """Return dummy NYSC verification for testing."""

    mismatches = {}

    if callup_no != DUMMY_NYSC["callup_no"]:
        mismatches["callup_no"] = "Call-up Number does not match"
    if certificate_no != DUMMY_NYSC["certificate_no"]:
        mismatches["certificate_no"] = "Certificate Number does not match"
    if dob != DUMMY_NYSC["dob"]:
        mismatches["dob"] = "Date of Birth does not match"

    if mismatches:
        return jsonify({
            "http_code": 422,
            "success": False,
            "content": {
                "error_title": "Verification Failed",
                "error_message": "Some fields do not match",
                "mismatches": mismatches
            }
        }), 422

    #  All matched
    return jsonify({
        "http_code": 200,
        "success": True,
        "content": {
            "title": "NYSC CERTIFICATE VERIFICATION",
            "message": {
                "candidate_info": {
                    "name": DUMMY_NYSC["name"],
                    "dob": DUMMY_NYSC["dob"],
                    "callup_no": DUMMY_NYSC["callup_no"],
                    "certificate_no": DUMMY_NYSC["certificate_no"],
                    "status": DUMMY_NYSC["status"],
                }
            },
            "verified": True
        }
    }), 200
# ======= CONFIGURE THESE AFTER INSPECTING THE NYSC PAGE =======
# Example placeholder URLS that commonly appear—replace with actual action URL
NYSC_VERIFY_URL = "https://portal.nysc.org.ng/VerifyCertificate"  # ← REPLACE with actual form action
NYSC_PAGE_URL = "https://portal.nysc.org.ng/"  # page to GET first (cookies etc.)

# Exact form input names used by NYSC form. Replace with actual values you find in page source:
FORM_FIELD_CALLUP = "CallUpNumber"       # ← REPLACE with actual input name attribute
FORM_FIELD_CERT_NO = "CertificateNumber" # ← REPLACE with actual input name attribute
FORM_FIELD_DOB = "DateOfBirth"           # ← REPLACE with actual input name attribute
# =============================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Create a requests session with retries
def _create_session(retries=3, backoff=0.3, status_forcelist=(500,502,503,504)):
    s = requests.Session()
    retries_obj = Retry(total=retries, backoff_factor=backoff, status_forcelist=status_forcelist, allowed_methods=["GET","POST"])
    s.mount("https://", HTTPAdapter(max_retries=retries_obj))
    s.headers.update(HEADERS)
    return s

def _detect_captcha_or_block(text):
    """Basic detection heuristics for CAPTCHAs or bot-blocking pages."""
    t = text.lower()
    keywords = ["captcha", "robot", "verify you are human", "access denied", "cloudflare", "bot detection", "challenge"]
    return any(k in t for k in keywords)

def parse_nysc_html(html_text):
    """
    Generic parser that tries some common patterns and falls back to text heuristics.
    Update selectors after inspecting the real NYSC HTML.
    Returns dict of extracted fields (keys will vary).
    """
    soup = BeautifulSoup(html_text, "lxml")

    # Try to find a structured table first (common pattern)
    result = {}
    try:
        # Attempt common table id/class possibilities (update if you find actual id)
        table = soup.find("table", {"id": re.compile(r".*(Grid|Result|Verify).*", re.I)}) or soup.find("table", {"class": re.compile(r".*(grid|result|verify).*", re.I)})
        if table:
            # Collect rows where left cell is key and right cell is value
            for row in table.find_all("tr"):
                cells = row.find_all(["td","th"])
                if len(cells) >= 2:
                    key = cells[0].get_text(" ", strip=True)
                    val = cells[1].get_text(" ", strip=True)
                    if key:
                        result[key] = val
            if result:
                return result
    except Exception:
        logger.exception("Table parsing failed")

    # Fallback: search page for lines containing keywords
    text = soup.get_text(separator="\n")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        low = ln.lower()
        if ("name" in low and ":" in ln) or ("surname" in low and ":" in ln):
            k, v = ln.split(":", 1)
            result[k.strip()] = v.strip()
        if ("certificate" in low and ":" in ln) or ("certificate" in low and "-" in ln):
            parts = re.split(r':|-', ln, maxsplit=1)
            if len(parts) >= 2:
                result[parts[0].strip()] = parts[1].strip()
        if ("call" in low and ":" in ln) or ("call up" in low):
            parts = re.split(r':|-', ln, maxsplit=1)
            if len(parts) >= 2:
                result[parts[0].strip()] = parts[1].strip()

    # Provide small raw snippet if we got nothing
    if not result:
        result["raw_snippet"] = "\n".join(lines[:25])

    return result

def verify_nysc(callup_no=None, certificate_no=None, dob=None, timeout=20):
    """
    Public function for verifying NYSC credentials.
    At least callup_no or certificate_no should be provided.
    Returns: dict { success: bool, data: dict|None, error: str|None, raw: str|None }
    """
    if not (callup_no or certificate_no):
        return {"success": False, "error": "Provide callup_no or certificate_no"}

    session = _create_session()
    try:
        # Optional: GET the page first to obtain cookies, hidden fields, or anti-CSRF tokens.
        try:
            resp_get = session.get(NYSC_PAGE_URL, timeout=timeout)
            resp_get.raise_for_status()
        except Exception:
            # If GET fails, we still attempt to POST directly; some portals accept direct POSTs.
            logger.info("GET to NYSC page failed or skipped; attempting POST directly.")

        # Build POST payload using the configured field names
        payload = {}
        if callup_no:
            payload[FORM_FIELD_CALLUP] = callup_no
        if certificate_no:
            payload[FORM_FIELD_CERT_NO] = certificate_no
        if dob:
            payload[FORM_FIELD_DOB] = dob

        # POST to the form action URL
        resp = session.post(NYSC_VERIFY_URL, data=payload, timeout=timeout)
        resp.raise_for_status()
        html = resp.text

        # Detect bot protection
        if _detect_captcha_or_block(html):
            return {"success": False, "error": "Site requires CAPTCHA or bot protection. Manual verification required.", "raw": html[:2000]}

        # Parse
        parsed = parse_nysc_html(html)
        if not parsed or (len(parsed) == 1 and "raw_snippet" in parsed):
            # nothing parsed — return helpful debug info
            return {"success": False, "error": "Could not parse verification response. Page structure likely different.", "raw": parsed.get("raw_snippet") if isinstance(parsed, dict) else None}

        return {"success": True, "data": parsed}

    except requests.HTTPError as he:
        logger.exception("NYSC HTTP error")
        return {"success": False, "error": f"HTTP error: {str(he)}"
                }
    except Exception as e:
        logger.exception("NYSC unexpected error")
        return {"success": False, "error": f"Unexpected error: {str(e)}"
                }

# def verify_nysc(callup_no=None, certificate_no=None, dob=None):
#     """Simulated NYSC verification (with placeholder)."""
#     if not callup_no:
#         return {"success": False, "error": "callup_no is required"}

#     # Simulate POST to NYSC portal (placeholder response)
#     payload = {
#         FORM_FIELD_CALLUP: callup_no,
#         FORM_FIELD_CERT_NO: certificate_no or "N/A",
#         FORM_FIELD_DOB: dob or "N/A",
#     }

#     # Instead of scraping (since portal is down), return mocked response
#     fake_result = {
#         "Name": "John Doe",
#         "Call-up Number": callup_no,
#         "Certificate Number": certificate_no or "N/A",
#         "Date of Birth": dob or "N/A",
#         "Status": "Verified ✅ (placeholder)",
#     }

#     return {"success": True, "data": fake_result}