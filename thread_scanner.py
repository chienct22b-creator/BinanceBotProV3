from concurrent.futures import ThreadPoolExecutor, as_completed

import config

from binance_api import get_klines
from indicators import analyze_symbol


def scan_symbol(symbol, timeframe):

    try:

        klines = get_klines(
            symbol=symbol,
            interval=timeframe,
            limit=200
        )

        data = analyze_symbol(klines)

        data["symbol"] = symbol
        data["timeframe"] = timeframe

        return data

    except Exception as e:

        print(symbol, e)

        return None


def scan_parallel(symbols, timeframe):

    results = []

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

        total = len(futures)

        completed = 0

        for future in as_completed(futures):

            completed += 1

            symbol = futures[future]

            print(f"[{completed}/{total}] {symbol}")

            result = future.result()

            if result:

                results.append(result)

    return results