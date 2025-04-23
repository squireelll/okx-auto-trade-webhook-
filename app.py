from flask import Flask, request
import time, hmac, hashlib, json, requests, os

app = Flask(__name__)

API_KEY = os.getenv("OKX_API_KEY")
SECRET_KEY = os.getenv("OKX_SECRET_KEY")
PASSPHRASE = os.getenv("OKX_PASSPHRASE")
BASE_URL = "https://www.okx.com"

def okx_sign(timestamp, method, path, body):
    msg = f"{timestamp}{method}{path}{body}"
    return hmac.new(SECRET_KEY.encode(), msg.encode(), hashlib.sha256).hexdigest()

def place_order(side, size="0.01", instId="BTC-USDT-SWAP"):
    timestamp = str(time.time())
    path = "/api/v5/trade/order"
    url = BASE_URL + path
    body_dict = {
        "instId": instId,
        "tdMode": "cross",
        "side": side,
        "ordType": "market",
        "sz": size
    }
    body = json.dumps(body_dict)
    sign = okx_sign(timestamp, "POST", path, body)
    headers = {
        "Content-Type": "application/json",
        "OK-ACCESS-KEY": API_KEY,
        "OK-ACCESS-SIGN": sign,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE
    }
    res = requests.post(url, headers=headers, data=body)
    return res.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    side = data.get("side")
    if side in ["buy", "sell"]:
        result = place_order(side)
        return result
    return {"error": "invalid signal"}

@app.route("/")
def home():
    return "✅ OKX Webhook Ready"
