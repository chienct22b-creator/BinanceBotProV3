from scanner import scan_market
from telegram_bot import send_signals

print("Đang quét thị trường...")

results = scan_market()

print(f"Đã quét {len(results)} tín hiệu")

send_signals(results)