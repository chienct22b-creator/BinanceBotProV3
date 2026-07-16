"""
====================================================
BinanceBotPro V3.2 Stable
Trade Tracker Engine
====================================================
"""

from binance.client import Client

import config

from database import (
    get_open_trades,
    close_trade,
)

from tracker_notifier import send_tracker_message


client = Client(
    config.API_KEY,
    config.API_SECRET
)


# ==================================================
# Lấy giá hiện tại
# ==================================================

def get_price(symbol):

    try:

        ticker = client.get_symbol_ticker(symbol=symbol)

        return float(ticker["price"])

    except Exception as e:

        print(f"[TRACKER] Price Error {symbol}: {e}")

        return None


# ==================================================
# Gửi Telegram
# ==================================================

def notify(symbol,
           direction,
           result,
           tp_level,
           entry,
           close_price):

    if result == "LOSS":

        title = "🛑 STOP LOSS"

    else:

        title = f"🎯 TP{tp_level} HIT"

    message = f"""
{title}

<b>{symbol}</b>

Direction : <b>{direction}</b>

Entry : <b>{entry:.6f}</b>

Close : <b>{close_price:.6f}</b>

Result : <b>{result}</b>
"""

    send_tracker_message(message)


# ==================================================
# Kiểm tra BUY
# ==================================================

def check_buy(trade):

    (
        trade_id,
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
        tp_level,
        open_price,
        close_price,
        close_time

    ) = trade

    price = get_price(symbol)

    if price is None:

        return

    # STOP LOSS

    if price <= sl:

        close_trade(
            trade_id,
            "LOSS",
            0,
            price
        )

        notify(
            symbol,
            direction,
            "LOSS",
            0,
            entry,
            price
        )

        print(f"[TRACKER] {symbol} STOP LOSS")

        return

    # TP3

    if price >= tp3:

        close_trade(
            trade_id,
            "WIN",
            3,
            price
        )

        notify(
            symbol,
            direction,
            "WIN",
            3,
            entry,
            price
        )

        print(f"[TRACKER] {symbol} TP3")

        return

    # TP2

    if price >= tp2:

        close_trade(
            trade_id,
            "WIN",
            2,
            price
        )

        notify(
            symbol,
            direction,
            "WIN",
            2,
            entry,
            price
        )

        print(f"[TRACKER] {symbol} TP2")

        return

    # TP1

    if price >= tp1:

        close_trade(
            trade_id,
            "WIN",
            1,
            price
        )

        notify(
            symbol,
            direction,
            "WIN",
            1,
            entry,
            price
        )

        print(f"[TRACKER] {symbol} TP1")


# ==================================================
# Kiểm tra SELL
# ==================================================

def check_sell(trade):

    (
        trade_id,
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
        tp_level,
        open_price,
        close_price,
        close_time

    ) = trade

    price = get_price(symbol)

    if price is None:

        return

    # STOP LOSS

    if price >= sl:

        close_trade(
            trade_id,
            "LOSS",
            0,
            price
        )

        notify(
            symbol,
            direction,
            "LOSS",
            0,
            entry,
            price
        )

        print(f"[TRACKER] {symbol} STOP LOSS")

        return

    # TP3

    if price <= tp3:

        close_trade(
            trade_id,
            "WIN",
            3,
            price
        )

        notify(
            symbol,
            direction,
            "WIN",
            3,
            entry,
            price
        )

        print(f"[TRACKER] {symbol} TP3")

        return

    # TP2

    if price <= tp2:

        close_trade(
            trade_id,
            "WIN",
            2,
            price
        )

        notify(
            symbol,
            direction,
            "WIN",
            2,
            entry,
            price
        )

        print(f"[TRACKER] {symbol} TP2")

        return

    # TP1

    if price <= tp1:

        close_trade(
            trade_id,
            "WIN",
            1,
            price
        )

        notify(
            symbol,
            direction,
            "WIN",
            1,
            entry,
            price
        )

        print(f"[TRACKER] {symbol} TP1")


# ==================================================
# Theo dõi toàn bộ lệnh
# ==================================================

def check_open_trades():

    trades = get_open_trades()

    print(f"[TRACKER] Open Trades: {len(trades)}")

    for trade in trades:

        try:

            direction = trade[4]

            if direction == "BUY":

                check_buy(trade)

            else:

                check_sell(trade)

        except Exception as e:

            print(f"[TRACKER ERROR] {e}")