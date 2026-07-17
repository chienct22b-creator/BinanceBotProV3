"""
====================================================
BinanceBotPro V3.4.0
Trade Tracker Engine
====================================================
"""

from datetime import datetime

from binance.client import Client

import config

from database import (
    PENDING,
    OPEN,
    CLOSED,
    STOPPED,
    EXPIRED,

    get_pending_trades,
    get_open_trades,

    mark_entry_filled,
    mark_stoploss,
    mark_expired,
    update_tp,
    close_trade
)

from tracker_notifier import send_tracker_message


client = Client(

    config.API_KEY,

    config.API_SECRET

)


# ==================================================
# Current Price
# ==================================================

def get_price(symbol):

    try:

        ticker = client.get_symbol_ticker(

            symbol=symbol

        )

        return float(

            ticker["price"]

        )

    except Exception as e:

        print(

            f"[TRACKER] Price Error {symbol}: {e}"

        )

        return None


# ==================================================
# Telegram Notify
# ==================================================

def notify(

    title,

    trade,

    price

):

    message = f"""

{title}

<b>{trade['symbol']}</b>

Direction : <b>{trade['direction']}</b>

Entry : <b>{trade['entry']:.6f}</b>

Price : <b>{price:.6f}</b>

Timeframe : <b>{trade['timeframe']}</b>

"""

    send_tracker_message(message)


# ==================================================
# Entry Filled Notify
# ==================================================

def notify_entry(

    trade,

    price

):

    notify(

        "🟢 ENTRY FILLED",

        trade,

        price

    )


# ==================================================
# TP Notify
# ==================================================

def notify_tp(

    trade,

    level,

    price

):

    notify(

        f"🎯 TP{level} HIT",

        trade,

        price

    )


# ==================================================
# Stop Loss Notify
# ==================================================

def notify_sl(

    trade,

    price

):

    notify(

        "🛑 STOP LOSS",

        trade,

        price

    )


# ==================================================
# Expired Notify
# ==================================================

def notify_expired(

    trade,

    price

):

    notify(

        "⌛ SIGNAL EXPIRED",

        trade,

        price

    )
# ==================================================
# Pending BUY
# ==================================================

def check_pending_buy(trade):

    price = get_price(trade["symbol"])

    if price is None:
        return

    entry_low = trade["entry_low"]
    entry_high = trade["entry_high"]

    # Giá vào vùng Entry
    if entry_low <= price <= entry_high:

        mark_entry_filled(
            trade["id"],
            price
        )

        notify_entry(
            trade,
            price
        )

        print(
            f"[TRACKER] {trade['symbol']} ENTRY FILLED"
        )


# ==================================================
# Pending SELL
# ==================================================

def check_pending_sell(trade):

    price = get_price(trade["symbol"])

    if price is None:
        return

    entry_low = trade["entry_low"]
    entry_high = trade["entry_high"]

    # Giá vào vùng Entry
    if entry_low <= price <= entry_high:

        mark_entry_filled(
            trade["id"],
            price
        )

        notify_entry(
            trade,
            price
        )

        print(
            f"[TRACKER] {trade['symbol']} ENTRY FILLED"
        )


# ==================================================
# Check Pending Trades
# ==================================================

def check_pending_trades():

    trades = get_pending_trades()

    print(f"[TRACKER] Pending Trades: {len(trades)}")

    for trade in trades:

        try:

            if trade["direction"] == "BUY":

                check_pending_buy(trade)

            else:

                check_pending_sell(trade)

        except Exception as e:

            print(f"[TRACKER ERROR] {e}")
# ==================================================
# OPEN BUY
# ==================================================

def check_open_buy(trade):

    price = get_price(trade["symbol"])

    if price is None:
        return

    # -----------------------------
    # Stop Loss
    # -----------------------------

    if price <= trade["sl"]:

        mark_stoploss(
            trade["id"],
            price
        )

        notify_sl(
            trade,
            price
        )

        print(
            f"[TRACKER] {trade['symbol']} STOP LOSS"
        )

        return

    # -----------------------------
    # TP1
    # -----------------------------

    if (
        price >= trade["tp1"]
        and trade["tp1_hit"] == 0
    ):

        update_tp(
            trade["id"],
            1
        )

        notify_tp(
            trade,
            1,
            price
        )

        print(
            f"[TRACKER] {trade['symbol']} TP1"
        )

    # -----------------------------
    # TP2
    # -----------------------------

    if (
        price >= trade["tp2"]
        and trade["tp2_hit"] == 0
    ):

        update_tp(
            trade["id"],
            2
        )

        notify_tp(
            trade,
            2,
            price
        )

        print(
            f"[TRACKER] {trade['symbol']} TP2"
        )

    # -----------------------------
    # TP3
    # -----------------------------

    if (
        price >= trade["tp3"]
        and trade["tp3_hit"] == 0
    ):

        update_tp(
            trade["id"],
            3
        )

        close_trade(

            trade["id"],

            CLOSED,

            3,

            price

        )

        notify_tp(

            trade,

            3,

            price

        )

        print(

            f"[TRACKER] {trade['symbol']} TP3 - CLOSED"

        )
# ==================================================
# OPEN SELL
# ==================================================

def check_open_sell(trade):

    price = get_price(trade["symbol"])

    if price is None:
        return

    # -----------------------------
    # Stop Loss
    # -----------------------------

    if price >= trade["sl"]:

        mark_stoploss(
            trade["id"],
            price
        )

        notify_sl(
            trade,
            price
        )

        print(
            f"[TRACKER] {trade['symbol']} STOP LOSS"
        )

        return

    # -----------------------------
    # TP1
    # -----------------------------

    if (
        price <= trade["tp1"]
        and trade["tp1_hit"] == 0
    ):

        update_tp(
            trade["id"],
            1
        )

        notify_tp(
            trade,
            1,
            price
        )

        print(
            f"[TRACKER] {trade['symbol']} TP1"
        )

    # -----------------------------
    # TP2
    # -----------------------------

    if (
        price <= trade["tp2"]
        and trade["tp2_hit"] == 0
    ):

        update_tp(
            trade["id"],
            2
        )

        notify_tp(
            trade,
            2,
            price
        )

        print(
            f"[TRACKER] {trade['symbol']} TP2"
        )

    # -----------------------------
    # TP3
    # -----------------------------

    if (
        price <= trade["tp3"]
        and trade["tp3_hit"] == 0
    ):

        update_tp(
            trade["id"],
            3
        )

        close_trade(

            trade["id"],

            CLOSED,

            3,

            price

        )

        notify_tp(

            trade,

            3,

            price

        )

        print(

            f"[TRACKER] {trade['symbol']} TP3 - CLOSED"

        )
# ==================================================
# Theo dõi Pending Trades
# ==================================================

def check_pending_trades():

    trades = get_pending_trades()

    if len(trades) > 0:

        print(f"[TRACKER] Pending Trades: {len(trades)}")

    for trade in trades:

        try:

            if trade["direction"] == "BUY":

                check_pending_buy(trade)

            else:

                check_pending_sell(trade)

        except Exception as e:

            print(f"[TRACKER ERROR] {e}")


# ==================================================
# Theo dõi Open Trades
# ==================================================

def check_open_trades():

    trades = get_open_trades()

    if len(trades) > 0:

        print(f"[TRACKER] Open Trades: {len(trades)}")

    for trade in trades:

        try:

            if trade["direction"] == "BUY":

                check_open_buy(trade)

            else:

                check_open_sell(trade)

        except Exception as e:

            print(f"[TRACKER ERROR] {e}")


# ==================================================
# Main Tracker
# ==================================================

def track_trades():

    try:

        # 1. Kiểm tra các tín hiệu đang chờ khớp Entry
        check_pending_trades()

        # 2. Kiểm tra các lệnh đã khớp Entry
        check_open_trades()

    except Exception as e:

        print(f"[TRACKER ERROR] {e}")