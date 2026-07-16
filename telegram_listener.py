"""
====================================================
BinanceBotPro V3.3
Telegram Listener
====================================================
"""

import requests

import config

from telegram_bot import send_message

from telegram_commands import (
    command_stats,
    command_today,
    command_open,
    command_help,
    command_ping,
    command_status,
    command_db,
)

# ==================================================
# Telegram Offset
# ==================================================

offset = 0


# ==================================================
# Lấy Update
# ==================================================

def get_updates():

    global offset

    url = (
        f"https://api.telegram.org/bot"
        f"{config.TELEGRAM_TOKEN}/getUpdates"
    )

    try:

        response = requests.get(

            url,

            params={

                "timeout": 2,

                "offset": offset

            },

            timeout=5

        )

        data = response.json()

        if not data.get("ok"):

            return []

        return data["result"]

    except Exception as e:

        print(f"[Telegram] {e}")

        return []


# ==================================================
# Xử lý Command
# ==================================================

def handle_command(text):

    text = text.strip().lower()

    if text == "/stats":

        send_message(command_stats())

    elif text == "/today":

        send_message(command_today())

    elif text == "/open":

        send_message(command_open())

    elif text == "/ping":

        send_message(command_ping())

    elif text == "/status":

        send_message(command_status())

    elif text == "/db":

        send_message(command_db())

    elif text == "/help":

        send_message(command_help())

    else:

        send_message(
            "❓ Không nhận diện được lệnh.\n"
            "Gõ /help để xem danh sách."
        )


# ==================================================
# Kiểm tra Telegram
# ==================================================

def check_commands():

    global offset

    updates = get_updates()

    if len(updates) == 0:

        return

    for update in updates:

        try:

            offset = update["update_id"] + 1

            if "message" not in update:

                continue

            message = update["message"]

            if "text" not in message:

                continue

            chat_id = str(message["chat"]["id"])

            if chat_id != str(config.CHAT_ID):

                continue

            text = message["text"]

            print(f"[Telegram] {text}")

            handle_command(text)

        except Exception as e:

            print(f"[Telegram] {e}")