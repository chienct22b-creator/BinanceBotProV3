import requests
from datetime import datetime

import config

from filters import filter_signals
from database import save_trade


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

        "SIDEWAY": "➡️",

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

    trend = coin["trend"]

    if isinstance(trend, dict):

        trend_text = trend.get(

            "trend_4h",

            "UNKNOWN"

        )

        strength = trend.get(

            "strength_4h",

            ""

        )

        confirmed = trend.get(

            "confirmed",

            False

        )

    else:

        trend_text = str(trend)

        strength = ""

        confirmed = True

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

        f"{trend_icon(trend_text)} "

        f"Trend : <b>{trend_text}</b>\n"

    )

    if strength:

        text += (

            f"💪 Strength : <b>{strength}</b>\n"

        )

    text += (

        f"✅ Confirmed : <b>{confirmed}</b>\n\n"

    )

    text += (

        f"💰 Price : <b>{coin['price']:.6f}</b>\n"

    )

    text += (

        f"📏 ATR : <b>{coin['indicator']['atr']:.6f}</b>\n\n"

    )

    text += (

        "🎯 <b>ENTRY ZONE</b>\n"

    )

    text += (

        f"{plan['entry_low']:.6f} ➜ {plan['entry_high']:.6f}\n\n"

    )

    text += (

        "🛑 <b>STOP LOSS</b>\n"

    )

    text += (

        f"{plan['sl']:.6f}\n\n"

    )

    text += (

        "🎯 <b>TAKE PROFIT</b>\n"

    )

    text += (

        f"TP1 : {plan['tp1']:.6f}\n"

    )

    text += (

        f"TP2 : {plan['tp2']:.6f}\n"

    )

    text += (

        f"TP3 : {plan['tp3']:.6f}\n\n"

    )

    text += (

        f"⚖️ RR : <b>1 : {plan['rr']}</b>\n"

    )

    if coin.get("volume_spike"):

        text += (

            "📦 Volume Spike\n"

        )

    text += "\n"

    text += (

        "📋 Indicators\n"

    )

    text += indicators

    return text


# ======================================================
# Send Signals
# ======================================================

def send_signals(results):

    buy_signals, sell_signals = filter_signals(results)

    print(f"results: {len(results)}")
    print(f"buy_signals: {len(buy_signals)}")
    print(f"sell_signals: {len(sell_signals)}")

    buy_list = []
    sell_list = []

    # ==========================================
    # BUY
    # ==========================================

    for coin in buy_signals:

        print("[BUY]", coin)

        save_trade(coin)

        buy_list.append(
            format_signal(coin)
        )

    # ==========================================
    # SELL
    # ==========================================

    for coin in sell_signals:

        print("[SELL]", coin)

        save_trade(coin)

        sell_list.append(
            format_signal(coin)
        )

    print(f"buy_list: {len(buy_list)}")
    print(f"sell_list: {len(sell_list)}")

    if len(buy_list) == 0 and len(sell_list) == 0:

        print("Không có tín hiệu mới.")

        return

    # ==========================================
    # Header
    # ==========================================

    header = ""

    header += (
        "🚀 <b>BINANCE BOT PRO V3.2</b>\n"
    )

    header += datetime.now().strftime(
        "🕒 %d/%m/%Y %H:%M:%S\n\n"
    )

    # ==========================================
    # Nội dung
    # ==========================================

    sections = []

    if buy_list:

        text = ""

        text += (
            f"🟢 <b>BUY ({len(buy_list)})</b>\n"
        )

        text += (
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        text += "\n\n".join(buy_list)

        sections.append(text)

    if sell_list:

        text = ""

        text += (
            f"🔴 <b>SELL ({len(sell_list)})</b>\n"
        )

        text += (
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        text += "\n\n".join(sell_list)

        sections.append(text)

    footer = ""

    footer += "\n\n"

    footer += (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
    )

    footer += (
        f"🟢 BUY : {len(buy_list)}\n"
    )

    footer += (
        f"🔴 SELL : {len(sell_list)}\n"
    )

    footer += (
        f"📊 TOTAL : {len(results)}"
    )

    # ==========================================
    # Telegram giới hạn 4096 ký tự
    # ==========================================

    current = header

    for section in sections:

        if len(current) + len(section) + len(footer) > 3900:

            current += footer

            send_message(current)

            current = header

        current += section + "\n\n"

    current += footer

    send_message(current)

    print("✅ Đã gửi Telegram.")