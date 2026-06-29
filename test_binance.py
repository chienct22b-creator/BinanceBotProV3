from binance_api import get_all_symbols

symbols = get_all_symbols()

print(f"Tổng số coin: {len(symbols)}")

print(symbols[:20])