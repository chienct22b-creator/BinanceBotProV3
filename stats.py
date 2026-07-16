"""
====================================================
BinanceBotPro V3.2 Stable
Statistics Engine
====================================================
"""

import sqlite3
from datetime import datetime

DB_NAME = "trades.db"


# ==================================================
# Kết nối Database
# ==================================================

def get_connection():

    return sqlite3.connect(DB_NAME)


# ==================================================
# Thống kê hôm nay
# ==================================================

def today_stats():

    conn = get_connection()

    cur = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cur.execute("""

    SELECT

        COUNT(*),

        SUM(CASE WHEN status='WIN' THEN 1 ELSE 0 END),

        SUM(CASE WHEN status='LOSS' THEN 1 ELSE 0 END),

        SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END),

        SUM(CASE WHEN tp_level=1 THEN 1 ELSE 0 END),

        SUM(CASE WHEN tp_level=2 THEN 1 ELSE 0 END),

        SUM(CASE WHEN tp_level=3 THEN 1 ELSE 0 END)

    FROM trades

    WHERE created_at LIKE ?

    """,

    (today + "%",)

    )

    row = cur.fetchone()

    conn.close()

    total = row[0] or 0
    win = row[1] or 0
    loss = row[2] or 0
    open_trade = row[3] or 0
    tp1 = row[4] or 0
    tp2 = row[5] or 0
    tp3 = row[6] or 0

    closed = win + loss

    if closed == 0:

        win_rate = 0

    else:

        win_rate = round(win * 100 / closed, 2)

    return {

        "total": total,

        "win": win,

        "loss": loss,

        "open": open_trade,

        "tp1": tp1,

        "tp2": tp2,

        "tp3": tp3,

        "win_rate": win_rate

    }


# ==================================================
# In thống kê
# ==================================================

def print_today_stats():

    s = today_stats()

    print()

    print("====================================")

    print("📊 BINANCE BOT PRO V3.2")

    print("====================================")

    print(f"Tổng lệnh : {s['total']}")

    print(f"OPEN      : {s['open']}")

    print(f"WIN       : {s['win']}")

    print(f"LOSS      : {s['loss']}")

    print()

    print(f"TP1 : {s['tp1']}")

    print(f"TP2 : {s['tp2']}")

    print(f"TP3 : {s['tp3']}")

    print()

    print(f"Win Rate : {s['win_rate']} %")

    print("====================================")

    print()


# ==================================================
# Trả về text Telegram
# ==================================================

def telegram_report():

    s = today_stats()

    text = ""

    text += "📊 <b>BINANCE BOT PRO V3.2</b>\n\n"

    text += f"📈 Tổng lệnh : <b>{s['total']}</b>\n"

    text += f"🟢 WIN : <b>{s['win']}</b>\n"

    text += f"🔴 LOSS : <b>{s['loss']}</b>\n"

    text += f"🟡 OPEN : <b>{s['open']}</b>\n\n"

    text += f"🎯 TP1 : {s['tp1']}\n"

    text += f"🎯 TP2 : {s['tp2']}\n"

    text += f"🏆 TP3 : {s['tp3']}\n\n"

    text += f"⭐ Win Rate : <b>{s['win_rate']}%</b>"

    return text
import requests
import config


# ==================================================
# Gửi báo cáo Telegram
# ==================================================

def send_daily_report():

    message = telegram_report()

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

        if response.status_code == 200:

            print("📊 Đã gửi báo cáo Telegram.")

        else:

            print(response.text)

    except Exception as e:

        print(e)