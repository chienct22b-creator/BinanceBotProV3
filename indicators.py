import pandas as pd

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import BollingerBands


def dataframe_from_klines(klines):
    """
    Chuyển dữ liệu nến Binance thành DataFrame.
    """

    df = pd.DataFrame(
        klines,
        columns=[
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore"
        ]
    )

    numeric = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    df[numeric] = df[numeric].astype(float)

    return df


# ===============================
# RSI
# ===============================

def calculate_rsi(df):

    rsi = RSIIndicator(
        close=df["close"],
        window=14
    )

    return float(round(rsi.rsi().iloc[-1], 2))


# ===============================
# EMA
# ===============================

def calculate_ema(df):

    ema20 = EMAIndicator(
        close=df["close"],
        window=20
    ).ema_indicator()

    ema50 = EMAIndicator(
        close=df["close"],
        window=50
    ).ema_indicator()

    ema200 = EMAIndicator(
        close=df["close"],
        window=200
    ).ema_indicator()

    return (
        float(round(ema20.iloc[-1], 4)),
        float(round(ema50.iloc[-1], 4)),
        float(round(ema200.iloc[-1], 4))
    )


# ===============================
# MACD
# ===============================

def calculate_macd(df):

    macd = MACD(df["close"])

    value = macd.macd().iloc[-1]

    signal = macd.macd_signal().iloc[-1]

    histogram = macd.macd_diff().iloc[-1]

    return (
        float(round(value, 4)),
        float(round(signal, 4)),
        float(round(histogram, 4))
    )


# ===============================
# Bollinger Bands
# ===============================

def calculate_bollinger(df):

    bb = BollingerBands(df["close"])

    upper = bb.bollinger_hband().iloc[-1]

    middle = bb.bollinger_mavg().iloc[-1]

    lower = bb.bollinger_lband().iloc[-1]

    return (
        float(round(upper, 4)),
        float(round(middle, 4)),
        float(round(lower, 4))
    )


# ===============================
# Trend
# ===============================

def calculate_trend(ema20, ema50, ema200):

    if ema20 > ema50 > ema200:
        return "UP"

    elif ema20 < ema50 < ema200:
        return "DOWN"

    return "SIDEWAYS"


# ===============================
# Score
# ===============================

def calculate_score(
        price,
        rsi,
        trend,
        histogram,
        bb_upper,
        bb_lower,
        ema20):

    score = 0

    signal_type = "NONE"

    # RSI
    if rsi <= 20:
        score += 30

    elif rsi >= 80:
        score += 30

    # Trend
    if trend == "UP":
        score += 20

    elif trend == "DOWN":
        score += 20

    # MACD
    if histogram > 0:
        score += 20

    # Bollinger
    if price <= bb_lower:
        score += 15

    elif price >= bb_upper:
        score += 15

    # EMA20
    if price > ema20:
        score += 15

    if score >= 70:

        if trend == "UP":
            signal_type = "BUY"

        elif trend == "DOWN":
            signal_type = "SELL"

    return score, signal_type


# ===============================
# Main Analyze
# ===============================

def analyze_symbol(klines):

    df = dataframe_from_klines(klines)

    price = float(round(df["close"].iloc[-1], 4))

    rsi = calculate_rsi(df)

    ema20, ema50, ema200 = calculate_ema(df)

    macd, signal, histogram = calculate_macd(df)

    bb_upper, bb_middle, bb_lower = calculate_bollinger(df)

    trend = calculate_trend(
        ema20,
        ema50,
        ema200
    )

    score, signal_type = calculate_score(
        price,
        rsi,
        trend,
        histogram,
        bb_upper,
        bb_lower,
        ema20
    )

    return {

        "price": price,

        "rsi": rsi,

        "ema20": ema20,
        "ema50": ema50,
        "ema200": ema200,

        "macd": macd,
        "signal": signal,
        "histogram": histogram,

        "bb_upper": bb_upper,
        "bb_middle": bb_middle,
        "bb_lower": bb_lower,

        "timeframe": "",

        "trend": trend,

        "score": score,

        "signal_type": signal_type

    }