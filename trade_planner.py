"""
====================================================
BinanceBotPro V3.1
Trade Planner
====================================================
"""

import config


# ==========================================
# Làm tròn theo giá
# ==========================================

def round_price(price):

    if price >= 1000:
        return round(price, 1)

    elif price >= 100:
        return round(price, 2)

    elif price >= 1:
        return round(price, 4)

    else:
        return round(price, 6)


# ==========================================
# BUY PLAN
# ==========================================

def build_buy_plan(indicator):

    price = indicator["price"]

    atr = indicator["atr"]

    ema20 = indicator["ema20"]

    # --------------------------------------
    # Entry
    # --------------------------------------

    if price > ema20 + atr * 0.5:

        entry_low = ema20

        entry_high = ema20 + atr * 0.25

    else:

        entry_low = price

        entry_high = price

    entry = (entry_low + entry_high) / 2

    # --------------------------------------
    # Stop Loss
    # --------------------------------------

    sl = entry - atr * config.ATR_SL_MULTIPLIER

    # --------------------------------------
    # Take Profit
    # --------------------------------------

    tp1 = entry + atr * config.ATR_TP1_MULTIPLIER

    tp2 = entry + atr * config.ATR_TP2_MULTIPLIER

    tp3 = entry + atr * config.ATR_TP3_MULTIPLIER

    # --------------------------------------
    # RR
    # --------------------------------------

    risk = entry - sl

    reward = tp2 - entry

    rr = reward / risk if risk > 0 else 0

    return {

        "entry_low": round_price(entry_low),

        "entry_high": round_price(entry_high),

        "entry": round_price(entry),

        "sl": round_price(sl),

        "tp1": round_price(tp1),

        "tp2": round_price(tp2),

        "tp3": round_price(tp3),

        "risk": round_price(risk),

        "reward": round_price(reward),

        "rr": round(rr, 2),

    }


# ==========================================
# SELL PLAN
# ==========================================

def build_sell_plan(indicator):

    price = indicator["price"]

    atr = indicator["atr"]

    ema20 = indicator["ema20"]

    if price < ema20 - atr * 0.5:

        entry_high = ema20

        entry_low = ema20 - atr * 0.25

    else:

        entry_low = price

        entry_high = price

    entry = (entry_low + entry_high) / 2

    sl = entry + atr * config.ATR_SL_MULTIPLIER

    tp1 = entry - atr * config.ATR_TP1_MULTIPLIER

    tp2 = entry - atr * config.ATR_TP2_MULTIPLIER

    tp3 = entry - atr * config.ATR_TP3_MULTIPLIER

    risk = sl - entry

    reward = entry - tp2

    rr = reward / risk if risk > 0 else 0

    return {

        "entry_low": round_price(entry_low),

        "entry_high": round_price(entry_high),

        "entry": round_price(entry),

        "sl": round_price(sl),

        "tp1": round_price(tp1),

        "tp2": round_price(tp2),

        "tp3": round_price(tp3),

        "risk": round_price(risk),

        "reward": round_price(reward),

        "rr": round(rr, 2),

    }


# ==========================================
# MAIN
# ==========================================

def calculate_trade_plan(indicator, direction):

    if direction == "BUY":

        plan = build_buy_plan(indicator)

    else:

        plan = build_sell_plan(indicator)

    plan["valid"] = plan["rr"] >= config.MIN_RR

    return plan