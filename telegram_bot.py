import requests
from datetime import datetime

import config

from filters import filter_signals
from notifier import should_notify


# ===================================
# Gửi 1 tin nhắn Telegram
# ===================================

def send_message(message):

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": config.CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
    )

    if response.status_code != 200:
        print("Lỗi gửi Telegram:", response.text)


# ===================================
# Định dạng 1 tín hiệu
# ===================================

def format_signal(coin):

    trend_icon = {
        "UP": "📈",
        "DOWN": "📉",
        "SIDEWAYS": "➡️"
    }

    return (
        f"<b>{coin['symbol']}</b>\n"
        f"💰 Giá: <b>{coin['price']}</b>\n"
        f"📊 RSI: <b>{coin['rsi']}</b>\n"
        f"{trend_icon.get(coin['trend'],'➡️')} Xu hướng: <b>{coin['trend']}</b>\n"
        f"⭐ Điểm: <b>{coin['score']}/100</b>\n"
        f"⏰ Khung: <b>{coin['timeframe']}</b>"
    )


# ===================================
# Gửi danh sách tín hiệu
# ===================================

def send_signals(results):

    buy_signals, sell_signals = filter_signals(results)

    buy_list = []

    sell_list = []

    # BUY
    for coin in buy_signals:

        if not should_notify(coin):
            continue

        buy_list.append(format_signal(coin))

    # SELL
    for coin in sell_signals:

        if not should_notify(coin):
            continue

        sell_list.append(format_signal(coin))

    if len(buy_list) == 0 and len(sell_list) == 0:

        print("Không có tín hiệu mới.")

        return

    message = "📊 <b>BINANCE SCANNER PRO V2</b>\n"

    message += f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"

    # BUY
    if buy_list:

        message += (
            f"🟢 <b>BUY SIGNALS ({len(buy_list)})</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
        )

        message += "\n\n".join(buy_list)

        message += "\n\n"

    # SELL
    if sell_list:

        message += (
            f"🔴 <b>SELL SIGNALS ({len(sell_list)})</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
        )

        message += "\n\n".join(sell_list)

        message += "\n\n"

    message += "━━━━━━━━━━━━━━━━━━\n"

    message += (
        f"📈 BUY : {len(buy_list)}\n"
        f"📉 SELL : {len(sell_list)}"
    )

    # Telegram giới hạn khoảng 4096 ký tự/tin nhắn
    if len(message) > 4000:
        message = message[:3900] + "\n\n... (Còn nhiều tín hiệu khác)"

    send_message(message)