from binance_api import get_klines
from indicators import analyze_symbol

klines = get_klines("BTCUSDT")

data = analyze_symbol(klines)

print(data)