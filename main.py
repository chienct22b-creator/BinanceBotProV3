import threading
import time
from datetime import datetime

import config

from database import init_database
from scanner import scan_market
from telegram_bot import send_signals
from telegram_listener import check_commands
from trade_tracker import track_trades
from stats import send_daily_report


last_report_day = None


# ==========================================================
# Banner
# ==========================================================

def banner():

    print("=" * 70)
    print("🚀 BinanceBotPro V3.4.0")
    print("📈 Multi-Timeframe Crypto Scanner")
    print("=" * 70)
    print(f"⏱ Scan Interval : {config.SCAN_INTERVAL}s")
    print(f"📊 Max Symbols   : {config.MAX_SYMBOLS}")
    print(f"⭐ Min Score     : {config.MIN_SCORE}/10")
    print(f"🧵 Threads       : {config.MAX_WORKERS}")
    print("=" * 70)


# ==========================================================
# Telegram Listener
# ==========================================================

def telegram_loop():

    print("🤖 Telegram Listener Started")

    while True:

        try:
            check_commands()

        except Exception as e:
            print(f"[Telegram] {e}")

        time.sleep(2)


# ==========================================================
# Main Loop
# ==========================================================

def main():

    global last_report_day

    # Khởi tạo database
    init_database()

    banner()

    # Telegram Listener
    telegram_thread = threading.Thread(
        target=telegram_loop,
        daemon=True
    )

    telegram_thread.start()

    while True:

        start = time.time()

        try:

            print()
            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] Đang quét thị trường..."
            )

            # ===============================
            # Scan Market
            # ===============================

            results = scan_market()

            print(f"✅ Tìm thấy {len(results)} tín hiệu.")

            if results:

                send_signals(results)

            else:

                print("Không có tín hiệu phù hợp.")

            # ===============================
            # Trade Tracker V3.4
            # ===============================

            track_trades()

            # ===============================
            # Daily Report
            # ===============================

            now = datetime.now()

            if now.hour == 23 and now.minute >= 59:

                if last_report_day != now.date():

                    print("📊 Gửi báo cáo cuối ngày...")

                    send_daily_report()

                    last_report_day = now.date()

        except KeyboardInterrupt:

            print("\n🛑 Bot đã dừng.")
            break

        except Exception as e:

            print(f"\n❌ Lỗi: {e}")

        elapsed = time.time() - start

        print(f"⏱ Thời gian quét: {elapsed:.2f} giây")
        print(f"⏳ Chờ {config.SCAN_INTERVAL} giây...\n")

        time.sleep(config.SCAN_INTERVAL)


# ==========================================================

if __name__ == "__main__":

    main()