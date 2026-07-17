"""
====================================================
BinanceBotPro V3.4.0
Database Engine
Trade Lifecycle Edition
====================================================
"""

import sqlite3
from datetime import datetime

DB_NAME = "trades.db"

# ==================================================
# Trade Status
# ==================================================

PENDING = "PENDING"      # Chưa khớp Entry
OPEN = "OPEN"            # Đã khớp Entry
CLOSED = "CLOSED"        # Hoàn thành
STOPPED = "STOPPED"      # Stop Loss
EXPIRED = "EXPIRED"      # Hết hạn


# ==================================================
# Kết nối Database
# ==================================================

def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


# ==================================================
# Thêm cột nếu chưa tồn tại
# ==================================================

def add_column_if_not_exists(conn, table, column, column_type):

    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table})")

    cols = [c[1] for c in cursor.fetchall()]

    if column not in cols:

        print(f"[DB] Add column: {column}")

        cursor.execute(

            f"""

            ALTER TABLE {table}

            ADD COLUMN {column} {column_type}

            """

        )

        conn.commit()


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

        entry_low REAL,

        entry_high REAL,

        sl REAL,

        tp1 REAL,

        tp2 REAL,

        tp3 REAL,

        rr REAL,

        status TEXT DEFAULT 'PENDING',

        tp_level INTEGER DEFAULT 0,

        open_price REAL,

        close_price REAL,

        filled_price REAL,

        filled_time TEXT,

        close_time TEXT,

        expired_time TEXT,

        tp1_hit INTEGER DEFAULT 0,

        tp2_hit INTEGER DEFAULT 0,

        tp3_hit INTEGER DEFAULT 0,

        sl_hit INTEGER DEFAULT 0

    )

    """)

    # =============================================
    # Auto Upgrade Database
    # =============================================

    add_column_if_not_exists(conn, "trades", "entry_low", "REAL")
    add_column_if_not_exists(conn, "trades", "entry_high", "REAL")

    add_column_if_not_exists(conn, "trades", "filled_price", "REAL")
    add_column_if_not_exists(conn, "trades", "filled_time", "TEXT")
    add_column_if_not_exists(conn, "trades", "expired_time", "TEXT")

    add_column_if_not_exists(conn, "trades", "tp1_hit", "INTEGER DEFAULT 0")
    add_column_if_not_exists(conn, "trades", "tp2_hit", "INTEGER DEFAULT 0")
    add_column_if_not_exists(conn, "trades", "tp3_hit", "INTEGER DEFAULT 0")

    add_column_if_not_exists(conn, "trades", "sl_hit", "INTEGER DEFAULT 0")

    conn.commit()

    conn.close()
# ==================================================
# Kiểm tra lệnh đã tồn tại
# ==================================================

def trade_exists(symbol, direction):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

    SELECT id

    FROM trades

    WHERE symbol=?
      AND direction=?
      AND status IN ('PENDING','OPEN')

    LIMIT 1

    """,

    (

        symbol,

        direction

    ))

    row = cur.fetchone()

    conn.close()

    return row is not None


# ==================================================
# Lưu tín hiệu mới
# ==================================================

def save_trade(signal):

    try:

        if trade_exists(
            signal["symbol"],
            signal["direction"]
        ):

            print(f"[DB] Đã tồn tại: {signal['symbol']}")

            return False

        plan = signal["trade_plan"]

        entry_low = float(plan["entry_low"])
        entry_high = float(plan["entry_high"])

        entry = (entry_low + entry_high) / 2

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

            entry_low,

            entry_high,

            sl,

            tp1,

            tp2,

            tp3,

            rr,

            status,

            open_price,

            filled_price,

            filled_time

        )

        VALUES(

            ?,?,?,?,?,?,
            ?,?,?,?,
            ?,?,?,?,
            ?,?,?

        )

        """,

        (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            signal["symbol"],

            signal["timeframe"],

            signal["direction"],

            signal["score"],

            entry,

            entry_low,

            entry_high,

            float(plan["sl"]),

            float(plan["tp1"]),

            float(plan["tp2"]),

            float(plan["tp3"]),

            float(plan["rr"]),

            PENDING,

            None,

            None,

            None

        ))

        conn.commit()

        conn.close()

        print(f"[DB] Đã lưu: {signal['symbol']}")

        return True

    except Exception as e:

        print(f"[DB ERROR] {e}")

        return False


# ==================================================
# Danh sách Pending
# ==================================================

def get_pending_trades():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM trades

    WHERE status='PENDING'

    ORDER BY created_at ASC

    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# ==================================================
# Danh sách Open
# ==================================================

def get_open_trades():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM trades

    WHERE status='OPEN'

    ORDER BY created_at ASC

    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# ==================================================
# Lấy 1 lệnh
# ==================================================

def get_trade(trade_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM trades

    WHERE id=?

    """,

    (

        trade_id,

    ))

    row = cur.fetchone()

    conn.close()

    return row
# ==================================================
# Entry Filled
# ==================================================

def mark_entry_filled(trade_id, price):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    UPDATE trades

    SET

        status=?,

        open_price=?,

        filled_price=?,

        filled_time=?

    WHERE id=?

    """,

    (

        OPEN,

        price,

        price,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        trade_id

    ))

    conn.commit()

    conn.close()


# ==================================================
# Update TP
# ==================================================

def update_tp(trade_id, level):

    conn = get_connection()

    cur = conn.cursor()

    field = f"tp{level}_hit"

    cur.execute(

        f"""

        UPDATE trades

        SET

            {field}=1,

            tp_level=?

        WHERE id=?

        """,

        (

            level,

            trade_id

        )

    )

    conn.commit()

    conn.close()


# ==================================================
# Stop Loss
# ==================================================

def mark_stoploss(trade_id, price):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    UPDATE trades

    SET

        status=?,

        sl_hit=1,

        close_price=?,

        close_time=?

    WHERE id=?

    """,

    (

        STOPPED,

        price,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        trade_id

    ))

    conn.commit()

    conn.close()


# ==================================================
# Signal Expired
# ==================================================

def mark_expired(trade_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    UPDATE trades

    SET

        status=?,

        expired_time=?

    WHERE id=?

    """,

    (

        EXPIRED,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        trade_id

    ))

    conn.commit()

    conn.close()


# ==================================================
# Close Trade
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

        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

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

    SELECT

        status,

        COUNT(*)

    FROM trades

    WHERE created_at LIKE ?

    GROUP BY status

    """,

    (

        today + "%",

    ))

    rows = cur.fetchall()

    conn.close()

    return rows


# ==================================================
# Đếm số lệnh theo trạng thái
# ==================================================

def count_by_status(status):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """

        SELECT COUNT(*)

        FROM trades

        WHERE status=?

        """,

        (

            status,

        )

    )

    total = cur.fetchone()[0]

    conn.close()

    return total


# ==================================================
# Lấy lệnh gần nhất
# ==================================================

def get_last_trade(symbol):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """

        SELECT *

        FROM trades

        WHERE symbol=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            symbol,

        )

    )

    row = cur.fetchone()

    conn.close()

    return row


# ==================================================
# Xóa toàn bộ lệnh (Debug)
# ==================================================

def clear_database():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("DELETE FROM trades")

    conn.commit()

    conn.close()

    print("[DB] Database cleared.")


# ==================================================
# Khởi tạo Database khi import
# ==================================================

init_database()