from concurrent.futures import ThreadPoolExecutor, as_completed

import config

from binance_api import get_klines

from indicators import analyze_indicators
from signal_score import calculate_signal_score
from volume_filter import volume_spike


# ==========================================================
# Scan 1 symbol
# ==========================================================

def scan_symbol(symbol, timeframe):

    try:

        klines = get_klines(
            symbol=symbol,
            interval=timeframe,
            limit=250
        )

        if not klines:
            return None

        indicator = analyze_indicators(klines)

        if indicator is None:
            return None

        signal = calculate_signal_score(indicator)

        result = {

            "symbol": symbol,

            "timeframe": timeframe,

            "indicator": indicator,

            "signal": signal,

            "volume_spike": volume_spike(indicator),

        }

        return result

    except Exception as e:

        print(f"[ERROR] {symbol}: {e}")

        return None


# ==========================================================
# Parallel Scanner
# ==========================================================

def scan_parallel(symbols, timeframe):

    results = []

    total = len(symbols)

    completed = 0

    with ThreadPoolExecutor(
        max_workers=config.MAX_WORKERS
    ) as executor:

        futures = {

            executor.submit(
                scan_symbol,
                symbol,
                timeframe
            ): symbol

            for symbol in symbols

        }

        for future in as_completed(futures):

            completed += 1

            symbol = futures[future]

            print(
                f"[{completed}/{total}] "
                f"{symbol} "
                f"({timeframe})"
            )

            try:

                result = future.result()

                if result:

                    results.append(result)

            except Exception as e:

                print(

                    f"[THREAD ERROR] "

                    f"{symbol}: {e}"

                )

    return results