from email.utils import parseaddr


def analyze_headers(message):
    findings = []

    from_address = parseaddr(str(message.get("From", "")))[1].lower()
    reply_to = parseaddr(str(message.get("Reply-To", "")))[1].lower()
    return_path = parseaddr(str(message.get("Return-Path", "")))[1].lower()

    authentication_results = str(
        message.get("Authentication-Results", "")
    ).strip()

    received_spf = str(message.get("Received-SPF", "")).strip()

    if from_address and reply_to:
        from_domain = from_address.rsplit("@", 1)[-1]
        reply_domain = reply_to.rsplit("@", 1)[-1]

        if from_domain != reply_domain:
            findings.append({
                "indicator": "From and Reply-To domains differ",
                "details": f"From: {from_domain}; Reply-To: {reply_domain}",
                "severity": "Review",
            })

    if not authentication_results:
        findings.append({
            "indicator": "Authentication-Results header missing",
            "details": "No recorded Authentication-Results header was found.",
            "severity": "Informational",
        })
    else:
        auth_lower = authentication_results.lower()

        for mechanism in ("spf", "dkim", "dmarc"):
            if mechanism in auth_lower:
                if f"{mechanism}=pass" in auth_lower:
                    result = "pass"
                elif f"{mechanism}=fail" in auth_lower:
                    result = "fail"
                elif f"{mechanism}=softfail" in auth_lower:
                    result = "softfail"
                elif f"{mechanism}=none" in auth_lower:
                    result = "none"
                else:
                    result = "recorded, exact result not identified"

                findings.append({
                    "indicator": f"{mechanism.upper()} result in header",
                    "details": result,
                    "severity": (
                        "Review" if result in ("fail", "softfail")
                        else "Informational"
                    ),
                })

    if received_spf:
        findings.append({
            "indicator": "Received-SPF header present",
            "details": received_spf,
            "severity": "Informational",
        })

    if return_path and from_address:
        from_domain = from_address.rsplit("@", 1)[-1]
        return_domain = return_path.rsplit("@", 1)[-1]

        if return_domain and return_domain != from_domain:
            findings.append({
                "indicator": "Return-Path and From domains differ",
                "details": f"From: {from_domain}; Return-Path: {return_domain}",
                "severity": "Review",
            })

    if not findings:
        findings.append({
            "indicator": "No configured header indicators detected",
            "details": "This does not establish that the email is legitimate.",
            "severity": "Informational",
        })

    return {
        "from_address": from_address,
        "reply_to": reply_to,
        "return_path": return_path,
        "authentication_results": authentication_results,
        "received_spf": received_spf,
        "dkim_signature_present": bool(message.get("DKIM-Signature")),
        "findings": findings,
    }
