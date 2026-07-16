"""
====================================================
BinanceBotPro V3.2
Tracker Notifier
====================================================
"""

import requests
import config


def send_tracker_message(message):

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"

    try:

        response = requests.post(

            url,

            data={

                "chat_id": config.CHAT_ID,

                "text": message,

                "parse_mode": "HTML"

            },

            timeout=20

        )

        if response.status_code != 200:

            print("[TRACKER] Telegram Error")

            print(response.text)

    except Exception as e:

        print(f"[TRACKER] {e}")