"""
====================================================
BinanceBotPro V3.1
Volume Filter Engine
====================================================
"""

from typing import List

import config


# ==========================================================
# Stablecoin và token không muốn quét
# ==========================================================

IGNORE = {

    "USDCUSDT",
    "BUSDUSDT",
    "FDUSDUSDT",
    "TUSDUSDT",
    "USDPUSDT",

}


# ==========================================================
# Token đòn bẩy cần loại bỏ
# ==========================================================

LEVERAGED_SUFFIX = (

    "UPUSDT",
    "DOWNUSDT",
    "BULLUSDT",
    "BEARUSDT",

)


# ==========================================================
# Chỉ lấy coin USDT
# ==========================================================

def filter_usdt(tickers: List):

    result = []

    for t in tickers:

        symbol = t["symbol"]

        # Chỉ lấy USDT
        if not symbol.endswith("USDT"):
            continue

        # Stablecoin
        if symbol in IGNORE:
            continue

        # Token đòn bẩy
        if symbol.endswith(LEVERAGED_SUFFIX):
            continue

        result.append(t)

    return result


# ==========================================================
# Lọc theo Quote Volume
# ==========================================================

def filter_quote_volume(

    tickers,

    min_quote_volume=None,

):

    if min_quote_volume is None:

        min_quote_volume = config.MIN_QUOTE_VOLUME

    result = []

    for t in tickers:

        try:

            volume = float(t["quoteVolume"])

        except Exception:

            continue

        if volume >= min_quote_volume:

            result.append(t)

    return result


# ==========================================================
# Sắp xếp theo Quote Volume giảm dần
# ==========================================================

def sort_volume(tickers):

    return sorted(

        tickers,

        key=lambda x: float(x["quoteVolume"]),

        reverse=True,

    )


# ==========================================================
# Lấy Top Volume Coin
# ==========================================================

def top_symbols(

    tickers,

    limit=None,

):

    if limit is None:

        limit = config.MAX_SYMBOLS

    tickers = filter_usdt(tickers)

    tickers = filter_quote_volume(

        tickers,

        config.MIN_QUOTE_VOLUME,

    )

    tickers = sort_volume(tickers)

    return [

        t["symbol"]

        for t in tickers[:limit]

    ]


# ==========================================================
# Kiểm tra Volume Spike
# ==========================================================

def volume_spike(indicator):

    try:

        volume = float(indicator["volume"])

        avg = float(indicator["volume_ma20"])

    except Exception:

        return False

    if avg <= 0:

        return False

    return volume >= avg * 1.5