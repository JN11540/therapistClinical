import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import qrcode as qrcode_lib


class QRCodeService:

    def __init__(self):
        self._secret = os.environ.get("SECRET_KEY", "")
        self._expiry_minutes = 10
        self._output_path = Path(__file__).parent / "patient_qrcode.png"

    def generate_sig(self, payload: dict) -> str:
        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        sig = hmac.new(
            self._secret.encode("utf-8"),
            payload_str.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        return base64.b64encode(sig).decode("utf-8")

    def generate_qrcode(
        self,
        data: dict,
    ) -> dict:
        expiry = (datetime.now(timezone.utc) + timedelta(minutes=self._expiry_minutes)).isoformat()
        payload = {"data": data, "expiry": expiry}
        sig = self.generate_sig(payload)
        payload_with_sig = {**payload, "sig": sig}

        qr_content = json.dumps(payload_with_sig, ensure_ascii=False)
        qr = qrcode_lib.QRCode(
            version=None,
            error_correction=qrcode_lib.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(self._output_path)

        return payload_with_sig
