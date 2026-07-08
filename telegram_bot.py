import requests
from datetime import datetime

import config


# ==========================================================
# Gửi Telegram
# ==========================================================

def send_message(message):

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"

    requests.post(

        url,

        data={

            "chat_id": config.CHAT_ID,

            "text": message,

            "parse_mode": "HTML"

        }

    )


# ==========================================================
# Format BUY / SELL
# ==========================================================

def format_signal(result):

    indicator = result["indicator"]

    trend = result["trend"]

    direction = result["direction"]

    score = result["score"]

    if direction == "BUY":

        icon = "🟢"

    else:

        icon = "🔴"

    volume = "YES" if result["volume_spike"] else "NO"

    message = f"""
{icon} <b>{direction}</b>

<b>{result['symbol']}</b>

💰 Price : <b>{indicator['price']:.6f}</b>

⭐ Score : <b>{score}/10</b>

⏰ TF : <b>{result['timeframe']}</b>

━━━━━━━━━━━━━━

📊 RSI : <b>{indicator['rsi']:.2f}</b>

📈 ADX : <b>{indicator['adx']:.2f}</b>

📦 Volume Spike : <b>{volume}</b>

━━━━━━━━━━━━━━

📈 Trend 15m : <b>{trend['trend_15m']}</b>

📈 Trend 1H : <b>{trend['trend_1h']}</b>

📈 Trend 4H : <b>{trend['trend_4h']}</b>

━━━━━━━━━━━━━━

EMA20 : {indicator['ema20']:.4f}

EMA50 : {indicator['ema50']:.4f}

EMA200 : {indicator['ema200']:.4f}

━━━━━━━━━━━━━━

<b>Conditions</b>

{", ".join(result["details"])}

━━━━━━━━━━━━━━

🕒 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""

    return message


# ==========================================================
# Gửi danh sách tín hiệu
# ==========================================================

def send_signals(results):

    if len(results) == 0:

        print("Không có tín hiệu.")

        return

    print(f"Gửi {len(results)} tín hiệu...")

    for signal in results:

        try:

            message = format_signal(signal)

            send_message(message)

        except Exception as e:

            print(e)