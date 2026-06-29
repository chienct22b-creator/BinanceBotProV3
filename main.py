import time
from datetime import datetime

from scanner import scan_market
from telegram_bot import send_signals


def main():

    print("=" * 60)
    print("🚀 BinanceBotProV2 Started")
    print("=" * 60)

    while True:

        try:

            print()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang quét thị trường...")

            results = scan_market()

            print(f"Đã phân tích {len(results)} tín hiệu")

            send_signals(results)

            print("✅ Hoàn thành.")

        except Exception as e:

            print("Lỗi:", e)

        print("⏳ Đợi 5 phút...\n")

        time.sleep(300)


if __name__ == "__main__":
    main()