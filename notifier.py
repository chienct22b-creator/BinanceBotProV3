from state import last_signals


def should_notify(coin):

    key = f"{coin['symbol']}_{coin['timeframe']}"

    current = coin["signal_type"]

    previous = last_signals.get(key)

    if previous == current:
        return False

    last_signals[key] = current

    return True