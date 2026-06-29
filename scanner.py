import config

from binance_api import get_all_symbols

from thread_scanner import scan_parallel


def scan_market():

    symbols = get_all_symbols()

    # Sau này sẽ thay bằng Top Volume
    symbols = symbols[:config.MAX_SYMBOLS]

    results = []

    for timeframe in config.TIMEFRAMES:

        print()

        print("=" * 60)

        print("TIMEFRAME:", timeframe)

        print("=" * 60)

        data = scan_parallel(
            symbols,
            timeframe
        )

        results.extend(data)

    return results