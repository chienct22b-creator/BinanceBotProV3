from scanner import scan_market

results = scan_market()

print()

print("=" * 60)

print("Tổng kết")

print("=" * 60)

print()

print(f"Số tín hiệu: {len(results)}")

print()

for coin in results[:15]:

    print(coin["symbol"])

    print("TF :", coin["timeframe"])

    print("Price :", coin["price"])

    print("RSI :", coin["rsi"])

    print("Trend :", coin["trend"])

    print("Score :", coin["score"])

    print("-------------------------")