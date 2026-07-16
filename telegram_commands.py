"""
====================================================
BinanceBotPro V3.3
Telegram Commands
====================================================
"""

import os
import sqlite3
from datetime import datetime

import config

from performance import performance_report
from database import get_open_trades

# ==================================================
# Thời gian khởi động Bot
# ==================================================

BOT_START_TIME = datetime.now()


# ==================================================
# /stats
# ==================================================

def command_stats():

    return performance_report()


# ==================================================
# /today
# ==================================================

def command_today():

    return performance_report()


# ==================================================
# /open
# ==================================================

def command_open():

    rows = get_open_trades()

    if len(rows) == 0:

        return "📭 <b>Không có lệnh đang mở.</b>"

    text = ""

    text += "📂 <b>OPEN TRADES</b>\n\n"

    for row in rows:

        text += (
            f"🪙 <b>{row[2]}</b>\n"
            f"📌 {row[4]}\n"
            f"💰 Entry : {row[5]:.6f}\n\n"
        )

    return text


# ==================================================
# /ping
# ==================================================

def command_ping():

    return (
        "🏓 <b>PONG</b>\n\n"
        "🟢 Bot đang hoạt động."
    )


# ==================================================
# /status
# ==================================================

def command_status():

    uptime = datetime.now() - BOT_START_TIME

    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60

    open_trades = len(get_open_trades())

    text = ""

    text += "🤖 <b>BOT STATUS</b>\n\n"

    text += "🟢 Status : Running\n"

    text += (
        f"⏱ Uptime : "
        f"{days}d {hours}h {minutes}m\n"
    )

    text += (
        f"📊 Scan Interval : "
        f"{config.SCAN_INTERVAL}s\n"
    )

    text += (
        f"📈 Open Trades : "
        f"{open_trades}\n"
    )

    text += (
        f"⭐ Min Score : "
        f"{config.MIN_SCORE}/10\n"
    )

    text += (
        f"🧵 Threads : "
        f"{config.MAX_WORKERS}\n"
    )

    text += (
        f"📊 Max Symbols : "
        f"{config.MAX_SYMBOLS}"
    )

    return text


# ==================================================
# /db
# ==================================================

def command_db():

    conn = sqlite3.connect("trades.db")

    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM trades"
    )

    total = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM trades WHERE status='OPEN'"
    )

    open_trade = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM trades WHERE status='WIN'"
    )

    win = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM trades WHERE status='LOSS'"
    )

    loss = cur.fetchone()[0]

    conn.close()

    if os.path.exists("trades.db"):

        size = os.path.getsize("trades.db") / 1024

    else:

        size = 0

    text = ""

    text += "💾 <b>DATABASE</b>\n\n"

    text += (
        f"📊 Total Trades : {total}\n"
    )

    text += (
        f"🟢 WIN : {win}\n"
    )

    text += (
        f"🔴 LOSS : {loss}\n"
    )

    text += (
        f"🟡 OPEN : {open_trade}\n"
    )

    text += (
        f"💽 Size : {size:.1f} KB"
    )

    return text


# ==================================================
# /help
# ==================================================

def command_help():

    return """
🤖 <b>BINANCE BOT PRO V3.3</b>

━━━━━━━━━━━━━━━━━━

📊 THỐNG KÊ

/stats

/today

/open

━━━━━━━━━━━━━━━━━━

⚙️ QUẢN TRỊ

/ping

/status

/db

/help

━━━━━━━━━━━━━━━━━━

🚀 BinanceBotPro V3.3
"""