import requests
from datetime import datetime

import config

from filters import filter_signals
from notifier import should_notify


# ======================================================
# Telegram Sender
# ======================================================

def send_message(message):

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(

        url,

        data={

            "chat_id": config.CHAT_ID,

            "text": message,

            "parse_mode": "HTML",

        },

        timeout=20,

    )

    if response.status_code != 200:

        print("Telegram Error:")

        print(response.text)


# ======================================================
# Quality
# ======================================================

def get_quality(score):

    if score >= 9:
        return "🏆 A+"

    elif score == 8:
        return "🥇 A"

    elif score == 7:
        return "🥈 B+"

    elif score == 6:
        return "🥉 B"

    return "C"


# ======================================================
# Trend Icon
# ======================================================

def trend_icon(trend):

    icons = {

        "UP": "📈",

        "DOWN": "📉",

        "SIDEWAYS": "➡️",

    }

    return icons.get(trend, "➡️")


# ======================================================
# Direction Icon
# ======================================================

def direction_icon(direction):

    if direction == "BUY":

        return "🟢"

    return "🔴"


# ======================================================
# Format Signal
# ======================================================

def format_signal(coin):

    plan = coin["trade_plan"]

    indicators = " • ".join(
        coin["details"]
    )

    text = ""

    text += (
        f"{direction_icon(coin['direction'])} "
        f"<b>{coin['direction']} {coin['symbol']}</b>\n\n"
    )

    text += (
        f"🏅 Quality : <b>{get_quality(coin['score'])}</b>\n"
    )

    text += (
        f"⭐ Score : <b>{coin['score']}/10</b>\n"
    )

    text += (
        f"{trend_icon(coin['trend'])} "
        f"Trend : <b>{coin['trend']}</b>\n\n"
    )

    text += (
        f"💰 Price : <b>{coin['price']}</b>\n"
    )

    text += (
        f"📏 ATR : <b>{coin['indicator']['atr']:.4f}</b>\n\n"
    )

    text += (
        "🎯 <b>ENTRY</b>\n"
    )

    text += (
        f"{plan['entry_low']}  ➜  {plan['entry_high']}\n\n"
    )

    text += (
        "🛑 <b>STOP LOSS</b>\n"
    )

    text += (
        f"{plan['sl']}\n\n"
    )

    text += (
        "🎯 <b>TAKE PROFIT</b>\n"
    )

    text += (
        f"TP1 : {plan['tp1']}\n"
    )

    text += (
        f"TP2 : {plan['tp2']}\n"
    )

    text += (
        f"TP3 : {plan['tp3']}\n\n"
    )

    text += (
        f"⚖️ RR : <b>1 : {plan['rr']}</b>\n"
    )

    if coin["volume_spike"]:

        text += (
            "📦 Volume Spike\n"
        )

    text += "\n"

    text += (
        f"📋 Indicators\n"
    )

    text += indicators

    return text


# ======================================================
# Send Signals
# ======================================================

def send_signals(results):

    buy_signals, sell_signals = filter_signals(results)

    buy_list = []

    sell_list = []

    # BUY

    for coin in buy_signals:

        if not should_notify(coin):

            continue

        buy_list.append(

            format_signal(coin)

        )

    # SELL

    for coin in sell_signals:

        if not should_notify(coin):

            continue

        sell_list.append(

            format_signal(coin)

        )

    if len(buy_list) == 0 and len(sell_list) == 0:

        print("Không có tín hiệu mới.")

        return

    message = ""

    message += (
        "🚀 <b>BINANCE BOT PRO V3.1</b>\n"
    )

    message += (
        datetime.now().strftime(
            "🕒 %d/%m/%Y %H:%M:%S\n\n"
        )
    )

    if buy_list:

        message += (
            f"🟢 <b>BUY ({len(buy_list)})</b>\n"
        )

        message += (
            "━━━━━━━━━━━━━━━━━━\n\n"
        )

        message += "\n\n".join(
            buy_list
        )

        message += "\n\n"

    if sell_list:

        message += (
            f"🔴 <b>SELL ({len(sell_list)})</b>\n"
        )

        message += (
            "━━━━━━━━━━━━━━━━━━\n\n"
        )

        message += "\n\n".join(
            sell_list
        )

        message += "\n\n"

    message += (
        "━━━━━━━━━━━━━━━━━━\n"
    )

    message += (
        f"🟢 BUY : {len(buy_list)}\n"
    )

    message += (
        f"🔴 SELL : {len(sell_list)}"
    )

    # Telegram giới hạn khoảng 4096 ký tự
    if len(message) > 4000:

        message = (
            message[:3900]
            + "\n\n...(Còn nhiều tín hiệu)"
        )

    send_message(message)