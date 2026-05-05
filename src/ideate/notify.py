from __future__ import annotations

import os
import smtplib
import warnings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_quality_email(idea_title: str, score_doc: str, improvement_doc: str) -> None:
    """Send a POC quality report by SMTP.

    Reads connection details from environment variables:
        SMTP_HOST           — required
        SMTP_PORT           — optional, defaults to 587
        SMTP_USER           — required
        SMTP_PASS           — required
        IDEATE_EMAIL_FROM   — optional, falls back to SMTP_USER
        IDEATE_EMAIL_TO     — required (recipient address)

    Silently no-ops if any required variable is absent.
    Emits a warning on send failure rather than raising.
    """
    host = os.environ.get("SMTP_HOST")
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    to_addr = os.environ.get("IDEATE_EMAIL_TO")
    from_addr = os.environ.get("IDEATE_EMAIL_FROM") or user or ""

    if not all([host, user, password, to_addr]):
        return  # SMTP not configured — skip silently

    port = int(os.environ.get("SMTP_PORT", "587"))
    subject = f"[ideate] POC Quality Report: {idea_title}"
    body = f"{score_doc}\n\n---\n\n{improvement_doc}"

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(host, port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(user, password)
            smtp.sendmail(from_addr, [to_addr], msg.as_string())
    except Exception as exc:  # noqa: BLE001
        warnings.warn(f"[ideate] email notification failed: {exc}", stacklevel=2)
