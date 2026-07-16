"""
====================================================
BinanceBotPro V3.2
Signal Filter
====================================================
"""

import config


def is_buy_signal(coin):

    if coin["score"] < config.MIN_SCORE:
        return False

    if coin["direction"] != "BUY":
        return False

    return True


def is_sell_signal(coin):

    if coin["score"] < config.MIN_SCORE:
        return False

    if coin["direction"] != "SELL":
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