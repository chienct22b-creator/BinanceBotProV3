"""
====================================================
BinanceBotPro V3.4.0
Telegram Commands Engine
====================================================
"""

import os
import sqlite3
from datetime import datetime

import config

from performance import performance_report
from database import (
    get_connection,
    get_open_trades,
)

# ==================================================
# Bot Start Time
# ==================================================

BOT_START_TIME = datetime.now()


# ==================================================
# Database Statistics
# ==================================================

def database_statistics():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT

            COUNT(*),

            SUM(CASE WHEN status='PENDING' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='CLOSED' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='STOPPED' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='EXPIRED' THEN 1 ELSE 0 END),

            SUM(tp1_hit),

            SUM(tp2_hit),

            SUM(tp3_hit)

        FROM trades

    """)

    row = cur.fetchone()

    conn.close()

    return {

        "total": row[0] or 0,

        "pending": row[1] or 0,

        "open": row[2] or 0,

        "closed": row[3] or 0,

        "stopped": row[4] or 0,

        "expired": row[5] or 0,

        "tp1": row[6] or 0,

        "tp2": row[7] or 0,

        "tp3": row[8] or 0,

    }


# ==================================================
# /stats
# ==================================================
def command_stats():

    return performance_report()


# ==================================================
# /today
# ==================================================

def command_today():

    stats = database_statistics()

    finished = (
        stats["closed"] +
        stats["stopped"]
    )

    if finished == 0:

        win_rate = 0.0

    else:

        win_rate = (
            stats["closed"] * 100 / finished
        )

    text = ""

    text += "📅 <b>TODAY REPORT</b>\n\n"

    text += (
        f"📨 Signals : <b>{stats['total']}</b>\n\n"
    )

    text += (
        f"🟡 Pending : <b>{stats['pending']}</b>\n"
    )

    text += (
        f"🟢 Open : <b>{stats['open']}</b>\n"
    )

    text += (
        f"🏆 Closed : <b>{stats['closed']}</b>\n"
    )

    text += (
        f"🛑 Stopped : <b>{stats['stopped']}</b>\n"
    )

    text += (
        f"⌛ Expired : <b>{stats['expired']}</b>\n"
    )

    text += (
        "━━━━━━━━━━━━━━━━━━\n"
    )

    text += (
        f"🎯 TP1 : <b>{stats['tp1']}</b>\n"
    )

    text += (
        f"🎯 TP2 : <b>{stats['tp2']}</b>\n"
    )

    text += (
        f"🎯 TP3 : <b>{stats['tp3']}</b>\n"
    )

    text += (
        "━━━━━━━━━━━━━━━━━━\n"
    )

    text += (
        f"📈 Win Rate : <b>{win_rate:.2f}%</b>\n"
    )

    text += (
        datetime.now().strftime(
            "🕒 %d/%m/%Y %H:%M"
        )
    )

    return text


# ==================================================
# /open
# ==================================================
def command_open():

    rows = get_open_trades()

    if not rows:

        return "📭 <b>Không có lệnh đang OPEN.</b>"

    text = ""

    text += "📂 <b>OPEN TRADES</b>\n"

    text += "━━━━━━━━━━━━━━━━━━\n\n"

    for row in rows:

        trade_id = row[0]
        symbol = row[2]
        timeframe = row[3]
        direction = row[4]
        entry = row[6]
        score = row[5]

        text += (
            f"🪙 <b>{symbol}</b>\n"
        )

        text += (
            f"📈 {direction} | {timeframe}\n"
        )

        text += (
            f"⭐ Score : {score}\n"
        )

        text += (
            f"💰 Entry : {entry:.6f}\n"
        )

        text += (
            f"🆔 ID : {trade_id}\n\n"
        )

    return text


# ==================================================
# /pending
# ==================================================

def command_pending():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT

            id,
            symbol,
            timeframe,
            direction,
            score,
            entry

        FROM trades

        WHERE status='PENDING'

        ORDER BY created_at DESC

    """)

    rows = cur.fetchall()

    conn.close()

    if not rows:

        return "📭 <b>Không có lệnh PENDING.</b>"

    text = ""

    text += "🟡 <b>PENDING TRADES</b>\n"

    text += "━━━━━━━━━━━━━━━━━━\n\n"

    for row in rows:

        text += (
            f"🪙 <b>{row[1]}</b>\n"
            f"📈 {row[3]} | {row[2]}\n"
            f"⭐ Score : {row[4]}\n"
            f"💰 Entry : {row[5]:.6f}\n\n"
        )

    return text


# ==================================================
# /closed
# ==================================================

def command_closed():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT

            symbol,
            direction,
            tp_level,
            close_price,
            close_time

        FROM trades

        WHERE status='CLOSED'

        ORDER BY close_time DESC

        LIMIT 10

    """)

    rows = cur.fetchall()

    conn.close()

    if not rows:

        return "📭 <b>Chưa có lệnh CLOSED.</b>"

    text = ""

    text += "🏆 <b>LAST CLOSED TRADES</b>\n"

    text += "━━━━━━━━━━━━━━━━━━\n\n"

    for row in rows:

        text += (
            f"🪙 <b>{row[0]}</b>\n"
            f"📈 {row[1]}\n"
            f"🎯 TP{row[2]}\n"
            f"💰 {row[3]:.6f}\n"
            f"🕒 {row[4]}\n\n"
        )

    return text


# ==================================================
# /ping
# ==================================================
def command_ping():

    return (
        "🏓 <b>PONG</b>\n\n"
        "🟢 Bot đang hoạt động bình thường."
    )


# ==================================================
# /status
# ==================================================

def command_status():

    uptime = datetime.now() - BOT_START_TIME

    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60

    stats = database_statistics()

    text = ""

    text += "🤖 <b>BOT STATUS</b>\n\n"

    text += "🟢 Status : <b>Running</b>\n"

    text += (
        f"⏱ Uptime : "
        f"{days}d {hours}h {minutes}m\n\n"
    )

    text += (
        f"🟡 Pending : {stats['pending']}\n"
    )

    text += (
        f"🟢 Open : {stats['open']}\n"
    )

    text += (
        f"🏆 Closed : {stats['closed']}\n"
    )

    text += (
        f"🛑 Stopped : {stats['stopped']}\n"
    )

    text += (
        f"⌛ Expired : {stats['expired']}\n\n"
    )

    text += (
        f"📊 Scan Interval : {config.SCAN_INTERVAL}s\n"
    )

    text += (
        f"📈 Max Symbols : {config.MAX_SYMBOLS}\n"
    )

    text += (
        f"⭐ Min Score : {config.MIN_SCORE}/10\n"
    )

    text += (
        f"🧵 Threads : {config.MAX_WORKERS}"
    )

    return text


# ==================================================
# /db
# ==================================================

def command_db():

    stats = database_statistics()

    if os.path.exists("trades.db"):

        size = os.path.getsize("trades.db") / 1024

    else:

        size = 0

    text = ""

    text += "💾 <b>DATABASE</b>\n\n"

    text += (
        f"📊 Total : {stats['total']}\n"
    )

    text += (
        f"🟡 Pending : {stats['pending']}\n"
    )

    text += (
        f"🟢 Open : {stats['open']}\n"
    )

    text += (
        f"🏆 Closed : {stats['closed']}\n"
    )

    text += (
        f"🛑 Stopped : {stats['stopped']}\n"
    )

    text += (
        f"⌛ Expired : {stats['expired']}\n\n"
    )

    text += (
        f"🎯 TP1 : {stats['tp1']}\n"
    )

    text += (
        f"🎯 TP2 : {stats['tp2']}\n"
    )

    text += (
        f"🎯 TP3 : {stats['tp3']}\n\n"
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
🤖 <b>BINANCE BOT PRO V3.4.0</b>

━━━━━━━━━━━━━━━━━━

📊 THỐNG KÊ

/stats
Hiệu suất giao dịch

/today
Thống kê hôm nay

/open
Danh sách lệnh OPEN

/pending
Danh sách lệnh PENDING

/closed
10 lệnh CLOSED gần nhất

━━━━━━━━━━━━━━━━━━

⚙️ HỆ THỐNG

/status
Trạng thái Bot

/db
Thông tin Database

/ping
Kiểm tra Bot

/version
Phiên bản Bot

/help
Danh sách lệnh

━━━━━━━━━━━━━━━━━━

🚀 BinanceBotPro V3.4.0
"""


# ==================================================
# /version
# ==================================================

def command_version():

    return (
        "🚀 <b>BinanceBotPro V3.4.0</b>\n\n"
        "Trade Lifecycle Edition\n\n"
        "✅ Pending Entry\n"
        "✅ Open Position\n"
        "✅ TP1 / TP2 / TP3 Tracking\n"
        "✅ Stop Loss Tracking\n"
        "✅ Auto Expired\n"
        "✅ Daily Statistics\n"
        "✅ Telegram Commands\n"
    )