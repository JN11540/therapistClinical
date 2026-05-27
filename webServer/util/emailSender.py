import json
import os
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from core.config import TREATMENT_JSON


class EmailSender:

    def __init__(self):
        self.sender_email   = os.environ.get("EMAIL_SENDER", "")
        self.sender_password = os.environ.get("EMAIL_PASSWORD", "")
        self.smtp_server    = os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port      = int(os.environ.get("EMAIL_SMTP_PORT", 587))
        self._msg: MIMEMultipart | None = None

    def build_message(self, receiver_email: str, subject: str) -> None:
        self._msg = MIMEMultipart()
        self._msg["From"] = self.sender_email
        self._msg["To"] = receiver_email
        self._msg["Subject"] = subject

    def attach_body(self, body: str) -> None:
        self._msg.attach(MIMEText(body, "plain", "utf-8"))

    def attach_json(self, data: dict) -> None:
        raw = json.dumps(data, ensure_ascii=False, indent=2)
        TREATMENT_JSON.write_text(raw, encoding="utf-8")

        attachment = MIMEApplication(raw.encode("utf-8"), _subtype="json")
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=TREATMENT_JSON.name,
        )
        self._msg.attach(attachment)

    def send(self) -> None:
        receiver_email = self._msg["To"]
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, self._msg.as_string())
            print(f"已成功寄送至 {receiver_email}")
