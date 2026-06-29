from binance.client import Client
import config

# Khởi tạo Binance Client
client = Client(
    config.API_KEY,
    config.API_SECRET
)


def get_all_symbols():
    """
    Lấy tất cả các cặp USDT đang giao dịch.
    """

    info = client.get_exchange_info()

    symbols = []

    for s in info["symbols"]:

        if (
            s["quoteAsset"] == "USDT"
            and s["status"] == "TRADING"
        ):
            symbols.append(s["symbol"])

    return sorted(symbols)


def get_klines(symbol, interval="15m", limit=200):
    """
    Lấy dữ liệu nến.
    """

    return client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )


def get_price(symbol):
    """
    Lấy giá hiện tại.
    """

    ticker = client.get_symbol_ticker(symbol=symbol)

    return float(ticker["price"])