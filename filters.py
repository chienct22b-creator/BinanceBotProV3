def is_buy_signal(coin):

    if coin["score"] < 70:
        return False

    if coin["signal_type"] != "BUY":
        return False

    return True


def is_sell_signal(coin):

    if coin["score"] < 70:
        return False

    if coin["signal_type"] != "SELL":
        return False

    return True


def filter_signals(results):

    buy = []

    sell = []

    for coin in results:

        if is_buy_signal(coin):
            buy.append(coin)

        elif is_sell_signal(coin):
            sell.append(coin)

    return buy, sell