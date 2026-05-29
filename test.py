import json
import hmac
import hashlib
import qrcode
import base64
from datetime import datetime, timedelta, timezone
from PIL import Image


# ============================================================
# 設定：Secret Key（請換成你自己的金鑰，存在環境變數或 config）
# ============================================================
SECRET_KEY = "bd31e10e3121be9b9229589e076bc3199f1529a00badd75a91192694fc8dfcbf"


# ============================================================
# 工具函數
# ============================================================

def generate_sig(payload: dict, secret: str) -> str:
    """
    用 HMAC-SHA256 對 payload 生成簽章
    """
    payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    sig = hmac.new(
        secret.encode("utf-8"),
        payload_str.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(sig).decode("utf-8")


def verify_sig(payload: dict, sig: str, secret: str) -> bool:
    """
    驗證簽章是否正確
    """
    expected_sig = generate_sig(payload, secret)
    return hmac.compare_digest(expected_sig, sig)


# ============================================================
# 1. 生成 QR Code
# ============================================================

def generate_qrcode(
    patient_id: str,
    expiry_hours: int = 72,
    output_path: str = "patient_qrcode.png"
) -> dict:
    """
    生成帶有 patient_id 和 expiry 的 QR Code

    Args:
        patient_id  : 個案 ID
        expiry_hours: QR Code 有效時數（預設 72 小時）
        output_path : 輸出圖片路徑

    Returns:
        payload dict（含 sig）
    """
    # 計算過期時間（UTC）
    expiry = (datetime.now(timezone.utc) + timedelta(hours=expiry_hours)).isoformat()

    # 組裝 payload（不含 sig）
    payload = {
        "patient_id": patient_id,
        "expiry": expiry,
    }

    # 加上簽章
    sig = generate_sig(payload, SECRET_KEY)
    payload_with_sig = {**payload, "sig": sig}

    # 轉成 JSON 字串
    qr_content = json.dumps(payload_with_sig, ensure_ascii=False)

    # 生成 QR Code 圖片
    qr = qrcode.QRCode(
        version=None,           # 自動選擇大小
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)

    return payload_with_sig


# ============================================================
# 2. 驗證掃描到的 QR Code 內容
# ============================================================

def verify_qrcode(qr_raw: str) -> dict:
    """
    驗證個案端 App 掃描後傳來的 QR Code 字串

    Args:
        qr_raw: 掃描到的原始字串

    Returns:
        {"valid": True, "patient_id": "..."} 或
        {"valid": False, "reason": "..."}
    """
    # 1. 解析 JSON
    try:
        data = json.loads(qr_raw)
    except json.JSONDecodeError:
        return {"valid": False, "reason": "QR Code 格式錯誤，無法解析 JSON"}

    # 2. 檢查必要欄位
    required_fields = ["patient_id", "expiry", "sig"]
    for field in required_fields:
        if field not in data:
            return {"valid": False, "reason": f"缺少必要欄位：{field}"}

    # 3. 驗證簽章
    payload = {
        "patient_id": data["patient_id"],
        "expiry": data["expiry"],
    }
    if not verify_sig(payload, data["sig"], SECRET_KEY):
        return {"valid": False, "reason": "簽章驗證失敗，QR Code 可能被竄改"}

    # 4. 驗證是否過期
    try:
        expiry_dt = datetime.fromisoformat(data["expiry"])
        now = datetime.now(timezone.utc)
        if now > expiry_dt:
            return {"valid": False, "reason": f"QR Code 已過期（expiry: {data['expiry']})"}
    except ValueError:
        return {"valid": False, "reason": "expiry 時間格式錯誤"}

    # 5. 驗證通過
    return {
        "valid": True,
        "patient_id": data["patient_id"],
        "expiry": data["expiry"],
    }


# ============================================================
# 3. Demo 執行
# ============================================================

if __name__ == "__main__":

    payload = generate_qrcode(
        patient_id="PAT-20260526-001",
        expiry_hours=72,
        output_path="patient_qrcode.png"
    )

    # print()
    # print("=" * 50)
    # print("【步驟 2】個案端 App — 掃描並驗證（模擬）")
    # print("=" * 50)

    # # 模擬 App 掃描後得到的字串
    # scanned_str = json.dumps(payload, ensure_ascii=False)

    # result = verify_qrcode(scanned_str)

    # if result["valid"]:
    #     print(f"✅ 驗證成功！")
    #     print(f"   patient_id : {result['patient_id']}")
    #     print(f"   expiry     : {result['expiry']}")
    #     print(f"   → 可以用 patient_id 呼叫 API 取得治療計畫")
    # else:
    #     print(f"❌ 驗證失敗：{result['reason']}")

    # print()
    # print("=" * 50)
    # print("【步驟 3】模擬驗證失敗情境")
    # print("=" * 50)

    # # 情境 A：竄改 patient_id
    # tampered = {**payload, "patient_id": "PAT-FAKE-999"}
    # result_a = verify_qrcode(json.dumps(tampered))
    # print(f"竄改 patient_id → {result_a}")

    # # 情境 B：過期的 QR Code
    # expired_payload = {
    #     "patient_id": "PAT-20260526-001",
    #     "expiry": "2020-01-01T00:00:00+00:00",
    # }
    # expired_payload["sig"] = generate_sig(
    #     {"patient_id": expired_payload["patient_id"], "expiry": expired_payload["expiry"]},
    #     SECRET_KEY
    # )
    # result_b = verify_qrcode(json.dumps(expired_payload))
    # print(f"過期 QR Code   → {result_b}")