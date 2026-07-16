"""
====================================================
BinanceBotPro V3.2
Database Engine
====================================================
"""

import sqlite3
from datetime import datetime

DB_NAME = "trades.db"


# ==================================================
# Kết nối
# ==================================================

def get_connection():
    return sqlite3.connect(DB_NAME)


# ==================================================
# Khởi tạo Database
# ==================================================

def init_database():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trades(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        created_at TEXT,

        symbol TEXT,

        timeframe TEXT,

        direction TEXT,

        score INTEGER,

        entry REAL,

        sl REAL,

        tp1 REAL,

        tp2 REAL,

        tp3 REAL,

        rr REAL,

        status TEXT,

        tp_level INTEGER DEFAULT 0,

        open_price REAL,

        close_price REAL,

        close_time TEXT

    )
    """)

    conn.commit()
    conn.close()


# ==================================================
# Kiểm tra trùng
# ==================================================

def trade_exists(symbol, direction):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id

        FROM trades

        WHERE symbol=?
        AND direction=?
        AND status='OPEN'

        LIMIT 1
        """,
        (symbol, direction)
    )

    row = cur.fetchone()

    conn.close()

    return row is not None


# ==================================================
# Lưu lệnh
# ==================================================

def save_trade(signal):

    try:

        if trade_exists(
            signal["symbol"],
            signal["direction"]
        ):
            print(f"[DB] Đã tồn tại: {signal['symbol']}")
            return

        plan = signal["trade_plan"]

        entry = (
            float(plan["entry_low"]) +
            float(plan["entry_high"])
        ) / 2

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""

        INSERT INTO trades(

            created_at,
            symbol,
            timeframe,
            direction,
            score,
            entry,
            sl,
            tp1,
            tp2,
            tp3,
            rr,
            status,
            open_price

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            signal["symbol"],

            signal["timeframe"],

            signal["direction"],

            signal["score"],

            entry,

            float(plan["sl"]),

            float(plan["tp1"]),

            float(plan["tp2"]),

            float(plan["tp3"]),

            float(plan["rr"]),

            "OPEN",

            entry

        ))

        conn.commit()

        print(f"[DB] Đã lưu: {signal['symbol']}")

        conn.close()

    except Exception as e:

        print(f"[DB ERROR] {e}")


# ==================================================
# Lệnh đang mở
# ==================================================

def get_open_trades():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM trades

    WHERE status='OPEN'

    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# ==================================================
# Đóng lệnh
# ==================================================

def close_trade(

    trade_id,

    status,

    tp_level,

    close_price

):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    UPDATE trades

    SET

        status=?,

        tp_level=?,

        close_price=?,

        close_time=?

    WHERE id=?

    """,

    (

        status,

        tp_level,

        close_price,

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        trade_id

    ))

    conn.commit()

    conn.close()


# ==================================================
# Thống kê hôm nay
# ==================================================

def today_statistics():

    conn = get_connection()

    cur = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cur.execute("""

    SELECT status,

           COUNT(*)

    FROM trades

    WHERE created_at LIKE ?

    GROUP BY status

    """,

    (today + "%",)

    )

    rows = cur.fetchall()

    conn.close()

    return rows
# ==================================================
# Lấy 1 lệnh theo ID
# ==================================================

def get_trade(trade_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM trades

    WHERE id=?

    """,

    (trade_id,))

    row = cur.fetchone()

    conn.close()

    return row