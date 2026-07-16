"""
====================================================
BinanceBotPro V3.3
Performance Engine
====================================================
"""

import sqlite3

DB_NAME = "trades.db"


# ==================================================
# Kết nối Database
# ==================================================

def get_connection():

    return sqlite3.connect(DB_NAME)
# ==================================================
# Tổng quan hiệu suất
# ==================================================

def summary():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT

        COUNT(*),

        SUM(CASE WHEN status='WIN' THEN 1 ELSE 0 END),

        SUM(CASE WHEN status='LOSS' THEN 1 ELSE 0 END),

        SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END)

    FROM trades

    """)

    row = cur.fetchone()

    conn.close()

    total = row[0] or 0
    win = row[1] or 0
    loss = row[2] or 0
    open_trade = row[3] or 0

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

        "win_rate": win_rate

    }
# ==================================================
# Tổng RR
# ==================================================

def total_rr():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT rr,status

    FROM trades

    WHERE status!='OPEN'

    """)

    rows = cur.fetchall()

    conn.close()

    rr = 0

    for value, status in rows:

        if status == "WIN":

            rr += value

        elif status == "LOSS":

            rr -= 1

    return round(rr, 2)
# ==================================================
# Thống kê theo từng Coin
# ==================================================

def coin_statistics():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT

        symbol,

        COUNT(*) as total,

        SUM(CASE WHEN status='WIN' THEN 1 ELSE 0 END) as win,

        SUM(CASE WHEN status='LOSS' THEN 1 ELSE 0 END) as loss,

        SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END) as open,

        SUM(CASE WHEN tp_level=1 THEN 1 ELSE 0 END) as tp1,

        SUM(CASE WHEN tp_level=2 THEN 1 ELSE 0 END) as tp2,

        SUM(CASE WHEN tp_level=3 THEN 1 ELSE 0 END) as tp3,

        SUM(
            CASE

                WHEN status='WIN' THEN rr

                WHEN status='LOSS' THEN -1

                ELSE 0

            END

        ) as total_rr

    FROM trades

    GROUP BY symbol

    ORDER BY total DESC

    """)

    rows = cur.fetchall()

    conn.close()

    data = []

    for row in rows:

        symbol = row[0]

        total = row[1] or 0

        win = row[2] or 0

        loss = row[3] or 0

        open_trade = row[4] or 0

        tp1 = row[5] or 0

        tp2 = row[6] or 0

        tp3 = row[7] or 0

        rr = round(row[8] or 0, 2)

        closed = win + loss

        if closed == 0:

            win_rate = 0

        else:

            win_rate = round(win * 100 / closed, 2)

        data.append({

            "symbol": symbol,

            "total": total,

            "win": win,

            "loss": loss,

            "open": open_trade,

            "tp1": tp1,

            "tp2": tp2,

            "tp3": tp3,

            "rr": rr,

            "win_rate": win_rate

        })

    return data
# ==================================================
# In thống kê Coin
# ==================================================

def print_coin_statistics():

    data = coin_statistics()

    print()

    print("============= COIN PERFORMANCE =============")

    for coin in data:

        print(

            f"{coin['symbol']:12}"

            f" WR:{coin['win_rate']:6}%"

            f" WIN:{coin['win']:3}"

            f" LOSS:{coin['loss']:3}"

            f" OPEN:{coin['open']:3}"

            f" RR:{coin['rr']:6}"

        )

    print("============================================")

    print()
# ==================================================
# Thống kê theo Timeframe
# ==================================================

def timeframe_statistics():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT

        timeframe,

        COUNT(*) as total,

        SUM(CASE WHEN status='WIN' THEN 1 ELSE 0 END),

        SUM(CASE WHEN status='LOSS' THEN 1 ELSE 0 END),

        SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END),

        SUM(CASE WHEN tp_level=1 THEN 1 ELSE 0 END),

        SUM(CASE WHEN tp_level=2 THEN 1 ELSE 0 END),

        SUM(CASE WHEN tp_level=3 THEN 1 ELSE 0 END),

        SUM(

            CASE

                WHEN status='WIN' THEN rr

                WHEN status='LOSS' THEN -1

                ELSE 0

            END

        )

    FROM trades

    GROUP BY timeframe

    ORDER BY timeframe

    """)

    rows = cur.fetchall()

    conn.close()

    data = []

    for row in rows:

        timeframe = row[0]

        total = row[1] or 0

        win = row[2] or 0

        loss = row[3] or 0

        open_trade = row[4] or 0

        tp1 = row[5] or 0

        tp2 = row[6] or 0

        tp3 = row[7] or 0

        rr = round(row[8] or 0, 2)

        closed = win + loss

        if closed == 0:
            win_rate = 0
        else:
            win_rate = round(win * 100 / closed, 2)

        data.append({

            "timeframe": timeframe,

            "total": total,

            "win": win,

            "loss": loss,

            "open": open_trade,

            "tp1": tp1,

            "tp2": tp2,

            "tp3": tp3,

            "rr": rr,

            "win_rate": win_rate

        })

    return data
# ==================================================
# In thống kê Timeframe
# ==================================================

def print_timeframe_statistics():

    data = timeframe_statistics()

    print()

    print("=========== TIMEFRAME PERFORMANCE ===========")

    for tf in data:

        print(

            f"{tf['timeframe']:6}"

            f" WR:{tf['win_rate']:6}%"

            f" WIN:{tf['win']:3}"

            f" LOSS:{tf['loss']:3}"

            f" OPEN:{tf['open']:3}"

            f" RR:{tf['rr']:6}"

        )

    print("=============================================")

    print()
# ==================================================
# Báo cáo hiệu suất tổng hợp
# ==================================================

def performance_report():

    s = summary()

    rr = total_rr()

    tf_data = timeframe_statistics()

    text = ""

    text += "📊 <b>BINANCE BOT PRO V3.3</b>\n"

    text += "=========================\n\n"

    text += f"📈 Total Signals : <b>{s['total']}</b>\n"

    text += f"🟢 WIN : <b>{s['win']}</b>\n"

    text += f"🔴 LOSS : <b>{s['loss']}</b>\n"

    text += f"🟡 OPEN : <b>{s['open']}</b>\n\n"

    text += f"⭐ Win Rate : <b>{s['win_rate']}%</b>\n"

    text += f"💰 Total RR : <b>{rr}R</b>\n\n"

    text += "📈 <b>TIMEFRAME</b>\n"

    for tf in tf_data:

        text += (
            f"\n{tf['timeframe']} | "
            f"WR {tf['win_rate']}% | "
            f"W:{tf['win']} "
            f"L:{tf['loss']} "
            f"O:{tf['open']} "
            f"RR:{tf['rr']}R"
        )

    return text