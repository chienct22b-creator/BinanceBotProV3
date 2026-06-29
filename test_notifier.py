from scanner import scan_market
from telegram_bot import send_signals

print("Lần quét thứ nhất")
results = scan_market("15m")
send_signals(results)

print("Lần quét thứ hai")
results = scan_market("15m")
send_signals(results)