"""
====================================================
BinanceBotPro V3.4.0 Final
Telegram Notification Engine
====================================================
"""

import requests
from datetime import datetime

import config

from filters import filter_signals
from database import save_trade


# ======================================================
# Telegram Sender
# ======================================================

def send_message(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{config.TELEGRAM_TOKEN}/sendMessage"
    )

    try:

        response = requests.post(

            url,

            data={

                "chat_id": config.CHAT_ID,

                "text": message,

                "parse_mode": "HTML",

                "disable_web_page_preview": True,

            },

            timeout=20,

        )

        if response.status_code != 200:

            print("[Telegram ERROR]")

            print(response.text)

    except Exception as e:

        print(f"[Telegram ERROR] {e}")


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

    return "⚪ C"


# ======================================================
# Trend Icon
# ======================================================

def trend_icon(trend):

    icons = {

        "UP": "📈",

        "DOWN": "📉",

        "SIDEWAY": "➡️",

        "SIDEWAYS": "➡️",

        "UNKNOWN": "❔",

    }

    return icons.get(trend, "➡️")


# ======================================================
# Direction Icon
# ======================================================

def direction_icon(direction):

    if direction == "BUY":

        return "🟢"

    elif direction == "SELL":

        return "🔴"

    return "⚪"


# ======================================================
# Status Icon
# ======================================================

def status_icon(status):

    icons = {

        "PENDING": "🟡",

        "OPEN": "🟢",

        "CLOSED": "🏁",

        "STOPPED": "🛑",

        "EXPIRED": "⌛",

    }

    return icons.get(status, "⚪")


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

        trend15 = trend.get(
            "trend_15m",
            "UNKNOWN"
        )

        trend1h = trend.get(
            "trend_1h",
            "UNKNOWN"
        )

        trend4h = trend.get(
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

        trend15 = str(trend)
        trend1h = "-"
        trend4h = "-"

        strength = ""
        confirmed = False

    text = ""

    # ==========================================
    # Tiêu đề
    # ==========================================

    text += (
        f"{direction_icon(coin['direction'])} "
        f"<b>{coin['direction']} {coin['symbol']}</b>\n\n"
    )

    text += (
        f"🏅 Quality : <b>{get_quality(coin['score'])}</b>\n"
    )

    text += (
        f"⭐ Score : <b>{coin['score']}/10</b>\n\n"
    )

    # ==========================================
    # Trend
    # ==========================================

    text += (
        "📈 <b>Trend</b>\n"
    )

    text += (
        f"{trend_icon(trend15)} 15m : <b>{trend15}</b>\n"
    )

    text += (
        f"{trend_icon(trend1h)} 1h : <b>{trend1h}</b>\n"
    )

    text += (
        f"{trend_icon(trend4h)} 4h : <b>{trend4h}</b>\n"
    )

    if strength:

        text += (
            f"💪 Strength : <b>{strength}</b>\n"
        )

    text += (
        f"✅ Confirmed : <b>{confirmed}</b>\n\n"
    )

    # ==========================================
    # Giá
    # ==========================================

    text += (
        f"💰 Price : <b>{coin['price']:.6f}</b>\n"
    )

    text += (
        f"📏 ATR : <b>{coin['indicator']['atr']:.6f}</b>\n\n"
    )

    # ==========================================
    # Trạng thái
    # ==========================================

    text += (
        f"{status_icon('PENDING')} "
        f"Status : <b>PENDING</b>\n\n"
    )

    # ==========================================
    # Entry
    # ==========================================

    text += (
        "🎯 <b>ENTRY ZONE</b>\n"
    )

    text += (
        f"{plan['entry_low']:.6f}"
        f" ➜ "
        f"{plan['entry_high']:.6f}\n\n"
    )

    # ==========================================
    # Stop Loss
    # ==========================================

    text += (
        "🛑 <b>STOP LOSS</b>\n"
    )

    text += (
        f"{plan['sl']:.6f}\n\n"
    )

    # ==========================================
    # Take Profit
    # ==========================================

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

    # ==========================================
    # RR
    # ==========================================

    text += (
        f"⚖️ RR : <b>1 : {plan['rr']}</b>\n"
    )

    # ==========================================
    # Volume Spike
    # ==========================================

    if coin.get("volume_spike"):

        text += "📦 Volume Spike\n"

    # ==========================================
    # Indicators
    # ==========================================

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

        try:

            # Lưu Database
            save_trade(coin)

            # Format Telegram
            buy_list.append(
                format_signal(coin)
            )

        except Exception as e:

            print(
                f"[BUY ERROR] "
                f"{coin['symbol']} : {e}"
            )

    # ==========================================
    # SELL
    # ==========================================

    for coin in sell_signals:

        print("[SELL]", coin)

        try:

            # Lưu Database
            save_trade(coin)

            # Format Telegram
            sell_list.append(
                format_signal(coin)
            )

        except Exception as e:

            print(
                f"[SELL ERROR] "
                f"{coin['symbol']} : {e}"
            )

    print(f"buy_list: {len(buy_list)}")
    print(f"sell_list: {len(sell_list)}")

    # ==========================================
    # Không có tín hiệu
    # ==========================================

    if not buy_list and not sell_list:

        print("Không có tín hiệu mới.")

        return

    # ==========================================
    # Header
    # ==========================================

    header = ""

    header += (
        "🚀 <b>BINANCE BOT PRO V3.4.0</b>\n"
    )

    header += datetime.now().strftime(
        "🕒 %d/%m/%Y %H:%M:%S\n\n"
    )

    sections = []

    # ==========================================
    # BUY Section
    # ==========================================

    if buy_list:

        buy_text = ""

        buy_text += (
            f"🟢 <b>BUY ({len(buy_list)})</b>\n"
        )

        buy_text += (
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        buy_text += "\n\n".join(buy_list)

        sections.append(buy_text)

    # ==========================================
    # SELL Section
    # ==========================================

    if sell_list:

        sell_text = ""

        sell_text += (
            f"🔴 <b>SELL ({len(sell_list)})</b>\n"
        )

        sell_text += (
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        sell_text += "\n\n".join(sell_list)

        sections.append(sell_text)

    # ==========================================
    # Footer
    # ==========================================

    footer = "\n\n"

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
        f"📊 TOTAL : {len(buy_list) + len(sell_list)}"
    )
    # ==========================================
    # Send Telegram
    # ==========================================

    message = header


    for section in sections:

        message += section

        message += "\n\n"



    message += footer



    # Giới hạn Telegram 4096 ký tự
    # tránh lỗi khi nhiều tín hiệu

    if len(message) > 4000:

        print(
            "[Telegram] Message too long, splitting..."
        )


        for section in sections:

            part = header + section + footer

            send_message(part)


    else:

        send_message(message)



    print(
        "✅ Telegram signal sent."
    )