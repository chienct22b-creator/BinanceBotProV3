from binance_api import get_all_tickers
from volume_filter import top_symbols

from thread_scanner import scan_parallel

from trend_filter import (
    check_trend,
    allow_buy,
    allow_sell,
)

from notifier import should_notify

import config


def scan_market():

    print("\nĐang lấy Top Volume...")

    tickers = get_all_tickers()

    symbols = top_symbols(
        tickers,
        limit=config.MAX_SYMBOLS,
    )

    print(f"Quét {len(symbols)} coin")

    tf_data = {}

    # ===============================
    # Scan từng timeframe
    # ===============================

    for tf in config.TIMEFRAMES:

        print(f"\n===== {tf} =====")

        tf_data[tf] = scan_parallel(
            symbols,
            tf,
        )

    # ===============================
    # Chuyển thành dictionary
    # ===============================

    tf15 = {

        x["symbol"]: x

        for x in tf_data["15m"]

    }

    tf1h = {

        x["symbol"]: x

        for x in tf_data["1h"]

    }

    tf4h = {

        x["symbol"]: x

        for x in tf_data["4h"]

    }

    results = []

    # ===============================
    # Ghép dữ liệu
    # ===============================

    for symbol in symbols:

        if symbol not in tf15:
            continue

        if symbol not in tf1h:
            continue

        if symbol not in tf4h:
            continue

        indicator15 = tf15[symbol]["indicator"]

        indicator1h = tf1h[symbol]["indicator"]

        indicator4h = tf4h[symbol]["indicator"]

        trend = check_trend(

            indicator15,

            indicator1h,

            indicator4h,

        )

        signal = tf15[symbol]["signal"]

        direction = signal["direction"]
        if direction == "NONE":
            continue

        score = signal["score"]

        if score < config.MIN_SCORE:
            continue

        if direction == "BUY":

            if not config.ENABLE_BUY:
                continue

            if not allow_buy(trend):
                continue

        elif direction == "SELL":

            if not config.ENABLE_SELL:
                continue

            if not allow_sell(trend):
                continue

        if not should_notify(

            symbol,

            "15m",

            direction,

            score,

            cooldown=config.COOLDOWN_MINUTES,

        ):

            continue

        results.append({

            "symbol": symbol,

            "direction": direction,

            "score": score,

            "price": indicator15["price"],

            "timeframe": "15m",

            "trend": trend,

            "indicator": indicator15,

            "details": signal["details"],

            "volume_spike": tf15[symbol]["volume_spike"],

        })

    print(f"\nTìm thấy {len(results)} tín hiệu")

    return results