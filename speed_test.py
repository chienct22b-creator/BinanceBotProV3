import time

from scanner import scan_market

start = time.time()

results = scan_market()

end = time.time()

print()

print("=" * 50)

print(f"Tổng tín hiệu: {len(results)}")

print(f"Thời gian: {end-start:.2f} giây")