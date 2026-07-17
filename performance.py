"""
====================================================
BinanceBotPro V3.4.0
Performance Engine
Trade Lifecycle Edition
====================================================
"""

import sqlite3

DB_NAME = "trades.db"


# ==================================================
# Trade Status
# ==================================================

PENDING = "PENDING"
OPEN = "OPEN"
CLOSED = "CLOSED"
STOPPED = "STOPPED"
EXPIRED = "EXPIRED"


# ==================================================
# Database Connection
# ==================================================

def get_connection():

    return sqlite3.connect(DB_NAME)


# ==================================================
# Summary Statistics
# ==================================================

def summary():

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
# Total RR
# ==================================================
def total_rr():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT rr, status

        FROM trades

        WHERE status IN ('CLOSED','STOPPED')

    """)

    rows = cur.fetchall()

    conn.close()

    rr = 0.0

    for value, status in rows:

        if status == CLOSED:

            rr += float(value or 0)

        elif status == STOPPED:

            rr -= 1

    return round(rr, 2)


# ==================================================
# Coin Statistics
# ==================================================

def coin_statistics():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT

            symbol,

            COUNT(*) as total,

            SUM(CASE WHEN status='PENDING' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='CLOSED' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='STOPPED' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='EXPIRED' THEN 1 ELSE 0 END),

            SUM(tp1_hit),

            SUM(tp2_hit),

            SUM(tp3_hit),

            SUM(
                CASE

                    WHEN status='CLOSED' THEN rr

                    WHEN status='STOPPED' THEN -1

                    ELSE 0

                END

            )

        FROM trades

        GROUP BY symbol

        ORDER BY total DESC

    """)

    rows = cur.fetchall()

    conn.close()

    data = []

    for row in rows:

        total = row[1] or 0

        closed = row[4] or 0

        stopped = row[5] or 0

        finished = closed + stopped

        if finished == 0:

            win_rate = 0

        else:

            win_rate = round(
                closed * 100 / finished,
                2
            )

        data.append({

            "symbol": row[0],

            "total": total,

            "pending": row[2] or 0,

            "open": row[3] or 0,

            "closed": closed,

            "stopped": stopped,

            "expired": row[6] or 0,

            "tp1": row[7] or 0,

            "tp2": row[8] or 0,

            "tp3": row[9] or 0,

            "rr": round(row[10] or 0, 2),

            "win_rate": win_rate,

        })

    return data


# ==================================================
# Print Coin Statistics
# ==================================================
def print_coin_statistics():

    data = coin_statistics()

    print()

    print("============== COIN PERFORMANCE ==============")

    for coin in data:

        print(

            f"{coin['symbol']:12}"

            f" WR:{coin['win_rate']:6}%"

            f" C:{coin['closed']:3}"

            f" S:{coin['stopped']:3}"

            f" O:{coin['open']:3}"

            f" P:{coin['pending']:3}"

            f" RR:{coin['rr']:6}"

        )

    print("==============================================")

    print()


# ==================================================
# Timeframe Statistics
# ==================================================

def timeframe_statistics():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT

            timeframe,

            COUNT(*) as total,

            SUM(CASE WHEN status='PENDING' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='CLOSED' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='STOPPED' THEN 1 ELSE 0 END),

            SUM(CASE WHEN status='EXPIRED' THEN 1 ELSE 0 END),

            SUM(tp1_hit),

            SUM(tp2_hit),

            SUM(tp3_hit),

            SUM(

                CASE

                    WHEN status='CLOSED' THEN rr

                    WHEN status='STOPPED' THEN -1

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

        total = row[1] or 0

        closed = row[4] or 0

        stopped = row[5] or 0

        finished = closed + stopped

        if finished == 0:

            win_rate = 0

        else:

            win_rate = round(

                closed * 100 / finished,

                2

            )

        data.append({

            "timeframe": row[0],

            "total": total,

            "pending": row[2] or 0,

            "open": row[3] or 0,

            "closed": closed,

            "stopped": stopped,

            "expired": row[6] or 0,

            "tp1": row[7] or 0,

            "tp2": row[8] or 0,

            "tp3": row[9] or 0,

            "rr": round(row[10] or 0, 2),

            "win_rate": win_rate,

        })

    return data


# ==================================================
# Print Timeframe Statistics
# ==================================================
def print_timeframe_statistics():

    data = timeframe_statistics()

    print()

    print("=========== TIMEFRAME PERFORMANCE ===========")

    for tf in data:

        print(

            f"{tf['timeframe']:6}"

            f" WR:{tf['win_rate']:6}%"

            f" C:{tf['closed']:3}"

            f" S:{tf['stopped']:3}"

            f" O:{tf['open']:3}"

            f" P:{tf['pending']:3}"

            f" RR:{tf['rr']:6}"

        )

    print("=============================================")

    print()


# ==================================================
# Performance Report
# ==================================================

def performance_report():

    s = summary()

    rr = total_rr()

    tf_data = timeframe_statistics()

    finished = s["closed"] + s["stopped"]

    if finished == 0:

        win_rate = 0

    else:

        win_rate = round(

            s["closed"] * 100 / finished,

            2

        )

    text = ""

    text += "📊 <b>BINANCE BOT PRO V3.4.0</b>\n"

    text += "━━━━━━━━━━━━━━━━━━\n\n"

    text += (

        f"📨 Total Signals : <b>{s['total']}</b>\n"

    )

    text += (

        f"🟡 Pending : <b>{s['pending']}</b>\n"

    )

    text += (

        f"🟢 Open : <b>{s['open']}</b>\n"

    )

    text += (

        f"🏆 Closed : <b>{s['closed']}</b>\n"

    )

    text += (

        f"🛑 Stopped : <b>{s['stopped']}</b>\n"

    )

    text += (

        f"⌛ Expired : <b>{s['expired']}</b>\n\n"

    )

    text += (

        f"🎯 TP1 : <b>{s['tp1']}</b>\n"

    )

    text += (

        f"🎯 TP2 : <b>{s['tp2']}</b>\n"

    )

    text += (

        f"🎯 TP3 : <b>{s['tp3']}</b>\n\n"

    )

    text += (

        f"⭐ Win Rate : <b>{win_rate}%</b>\n"

    )

    text += (

        f"💰 Total RR : <b>{rr}R</b>\n\n"

    )

    text += "📈 <b>TIMEFRAME PERFORMANCE</b>\n"
    for tf in tf_data:

        text += (

            f"\n<b>{tf['timeframe']}</b>\n"

        )

        text += (

            f"🏆 Closed : {tf['closed']} | "

            f"🛑 Stopped : {tf['stopped']}\n"

        )

        text += (

            f"🟢 Open : {tf['open']} | "

            f"🟡 Pending : {tf['pending']}\n"

        )

        text += (

            f"🎯 TP1:{tf['tp1']}  "

            f"TP2:{tf['tp2']}  "

            f"TP3:{tf['tp3']}\n"

        )

        text += (

            f"⭐ WR : {tf['win_rate']}%"

            f" | 💰 RR : {tf['rr']}R\n"

        )

        text += (

            "━━━━━━━━━━━━━━━━━━"

        )

    return text