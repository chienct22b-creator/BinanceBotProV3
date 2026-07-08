"""
====================================================
BinanceBotPro V3.2
Signal Score Engine
====================================================
"""


# ==================================================
# RSI
# ==================================================

def score_rsi(data):

    rsi = data["rsi"]

    if rsi <= 30:
        return 3, "BUY"

    elif rsi <= 35:
        return 2, "BUY"

    elif rsi >= 70:
        return 3, "SELL"

    elif rsi >= 65:
        return 2, "SELL"

    return 0, None


# ==================================================
# MACD
# ==================================================

def score_macd(data):

    macd = data["macd"]
    signal = data["macd_signal"]

    if macd > signal:
        return 2, "BUY"

    elif macd < signal:
        return 2, "SELL"

    return 0, None


# ==================================================
# EMA Trend
# ==================================================

def score_ema(data):

    ema20 = data["ema20"]
    ema50 = data["ema50"]
    ema200 = data["ema200"]

    if ema20 > ema50 > ema200:
        return 2, "BUY"

    elif ema20 < ema50 < ema200:
        return 2, "SELL"

    return 0, None


# ==================================================
# Bollinger Band
# ==================================================

def score_bollinger(data):

    price = data["price"]

    lower = data["bb_lower"]
    upper = data["bb_upper"]

    # Nới 1%

    if price <= lower * 1.01:
        return 1, "BUY"

    elif price >= upper * 0.99:
        return 1, "SELL"

    return 0, None


# ==================================================
# Volume Spike
# ==================================================

def score_volume(data):

    volume = data["volume"]
    average = data["volume_ma20"]

    if average <= 0:
        return 0

    if volume >= average * 1.5:
        return 1

    return 0


# ==================================================
# ADX
# ==================================================

def score_adx(data):

    adx = data["adx"]

    if adx >= 30:
        return 2

    elif adx >= 25:
        return 1

    return 0


# ==================================================
# Tổng hợp điểm
# ==================================================

def calculate_signal_score(data):

    buy = 0
    sell = 0

    buy_detail = []
    sell_detail = []

    # RSI

    score, signal = score_rsi(data)

    if signal == "BUY":
        buy += score
        buy_detail.append(f"RSI(+{score})")

    elif signal == "SELL":
        sell += score
        sell_detail.append(f"RSI(+{score})")

    # MACD

    score, signal = score_macd(data)

    if signal == "BUY":
        buy += score
        buy_detail.append("MACD(+2)")

    elif signal == "SELL":
        sell += score
        sell_detail.append("MACD(+2)")

    # EMA

    score, signal = score_ema(data)

    if signal == "BUY":
        buy += score
        buy_detail.append("EMA(+2)")

    elif signal == "SELL":
        sell += score
        sell_detail.append("EMA(+2)")

    # Bollinger

    score, signal = score_bollinger(data)

    if signal == "BUY":
        buy += score
        buy_detail.append("BB(+1)")

    elif signal == "SELL":
        sell += score
        sell_detail.append("BB(+1)")

    # Volume

    volume_score = score_volume(data)

    if volume_score:

        buy += volume_score
        sell += volume_score

        buy_detail.append("VOL(+1)")
        sell_detail.append("VOL(+1)")

    # ADX

    adx_score = score_adx(data)

    if adx_score:

        buy += adx_score
        sell += adx_score

        buy_detail.append(f"ADX(+{adx_score})")
        sell_detail.append(f"ADX(+{adx_score})")

    # ==========================
    # Quyết định
    # ==========================

    if buy > sell:

        return {

            "direction": "BUY",

            "score": buy,

            "details": buy_detail,

        }

    elif sell > buy:

        return {

            "direction": "SELL",

            "score": sell,

            "details": sell_detail,

        }

    return {

        "direction": "NONE",

        "score": buy,

        "details": [],

    }