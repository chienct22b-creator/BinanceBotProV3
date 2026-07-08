import pandas as pd

from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.volatility import BollingerBands, AverageTrueRange


# ==========================================================
# Chuẩn hóa dữ liệu Binance Klines
# ==========================================================

def prepare_dataframe(klines):

    columns = [
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base",
        "taker_buy_quote",
        "ignore",
    ]

    df = pd.DataFrame(
        klines,
        columns=columns,
    )

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce",
        )

    df = df.dropna()

    return df


# ==========================================================
# RSI
# ==========================================================

def calculate_rsi(df):

    rsi = RSIIndicator(
        close=df["close"],
        window=14,
    ).rsi()

    return float(rsi.iloc[-1])


# ==========================================================
# EMA
# ==========================================================

def calculate_ema(df):

    ema20 = EMAIndicator(
        close=df["close"],
        window=20,
    ).ema_indicator()

    ema50 = EMAIndicator(
        close=df["close"],
        window=50,
    ).ema_indicator()

    ema200 = EMAIndicator(
        close=df["close"],
        window=200,
    ).ema_indicator()

    return {

        "ema20": float(ema20.iloc[-1]),

        "ema50": float(ema50.iloc[-1]),

        "ema200": float(ema200.iloc[-1]),

    }


# ==========================================================
# MACD
# ==========================================================

def calculate_macd(df):

    macd = MACD(
        close=df["close"]
    )

    return {

        "macd": float(
            macd.macd().iloc[-1]
        ),

        "macd_signal": float(
            macd.macd_signal().iloc[-1]
        ),

        "macd_hist": float(
            macd.macd_diff().iloc[-1]
        ),

    }


# ==========================================================
# Bollinger Bands
# ==========================================================

def calculate_bollinger(df):

    bb = BollingerBands(

        close=df["close"],

        window=20,

        window_dev=2,

    )

    return {

        "bb_upper": float(
            bb.bollinger_hband().iloc[-1]
        ),

        "bb_middle": float(
            bb.bollinger_mavg().iloc[-1]
        ),

        "bb_lower": float(
            bb.bollinger_lband().iloc[-1]
        ),

    }


# ==========================================================
# ATR
# ==========================================================

def calculate_atr(df):

    atr = AverageTrueRange(

        high=df["high"],

        low=df["low"],

        close=df["close"],

        window=14,

    )

    return float(
        atr.average_true_range().iloc[-1]
    )


# ==========================================================
# ADX
# ==========================================================

def calculate_adx(df):

    adx = ADXIndicator(

        high=df["high"],

        low=df["low"],

        close=df["close"],

        window=14,

    )

    return float(
        adx.adx().iloc[-1]
    )


# ==========================================================
# STOCH RSI
# ==========================================================

def calculate_stoch_rsi(df):

    stoch = StochRSIIndicator(

        close=df["close"],

        window=14,

        smooth1=3,

        smooth2=3,

    )

    return {

        "stoch_k": float(
            stoch.stochrsi_k().iloc[-1]
        ),

        "stoch_d": float(
            stoch.stochrsi_d().iloc[-1]
        ),

    }


# ==========================================================
# VOLUME
# ==========================================================

def calculate_volume(df):

    volume_ma20 = (
        df["volume"]
        .rolling(20)
        .mean()
    )

    return {

        "volume": float(
            df["volume"].iloc[-1]
        ),

        "volume_ma20": float(
            volume_ma20.iloc[-1]
        ),

    }


# ==========================================================
# Indicator Engine
# ==========================================================

def analyze_indicators(klines):

    try:

        df = prepare_dataframe(klines)

        if len(df) < 200:
            return None

        data = {}

        data["price"] = float(
            df["close"].iloc[-1]
        )

        data["rsi"] = calculate_rsi(df)

        data["atr"] = calculate_atr(df)

        data["adx"] = calculate_adx(df)

        data.update(
            calculate_ema(df)
        )

        data.update(
            calculate_macd(df)
        )

        data.update(
            calculate_bollinger(df)
        )

        data.update(
            calculate_stoch_rsi(df)
        )

        data.update(
            calculate_volume(df)
        )

        return data

    except Exception as e:

        print("Indicator Error:", e)

        return None