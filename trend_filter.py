"""
====================================================
BinanceBotProV3
Trend Filter Engine
====================================================
"""

from typing import Dict


# ====================================================
# Xác định xu hướng bằng EMA
# ====================================================

def get_trend(indicator: Dict) -> str:

    ema20 = indicator["ema20"]
    ema50 = indicator["ema50"]
    ema200 = indicator["ema200"]

    if ema20 > ema50 > ema200:
        return "UP"

    if ema20 < ema50 < ema200:
        return "DOWN"

    return "SIDEWAY"


# ====================================================
# Độ mạnh xu hướng
# ====================================================

def trend_strength(indicator: Dict) -> str:

    adx = indicator["adx"]

    if adx >= 40:
        return "VERY_STRONG"

    elif adx >= 25:
        return "STRONG"

    elif adx >= 20:
        return "NORMAL"

    return "WEAK"


# ====================================================
# EMA có đang mở rộng không
# ====================================================

def ema_alignment(indicator: Dict) -> bool:

    ema20 = indicator["ema20"]
    ema50 = indicator["ema50"]
    ema200 = indicator["ema200"]

    diff1 = abs(ema20 - ema50)
    diff2 = abs(ema50 - ema200)

    return diff1 > 0 and diff2 > 0


# ====================================================
# Xác nhận đa khung thời gian
# ====================================================

def confirm_trend(
    trend_15m: str,
    trend_1h: str,
    trend_4h: str
) -> bool:

    if trend_15m == trend_1h == trend_4h:
        return True

    return False


# ====================================================
# Kiểm tra xu hướng hoàn chỉnh
# ====================================================

def check_trend(
    indicator_15m: Dict,
    indicator_1h: Dict,
    indicator_4h: Dict
) -> Dict:

    trend15 = get_trend(indicator_15m)
    trend1h = get_trend(indicator_1h)
    trend4h = get_trend(indicator_4h)

    confirmed = confirm_trend(
        trend15,
        trend1h,
        trend4h,
    )

    return {

        "trend_15m": trend15,

        "trend_1h": trend1h,

        "trend_4h": trend4h,

        "confirmed": confirmed,

        "strength_15m": trend_strength(indicator_15m),

        "strength_1h": trend_strength(indicator_1h),

        "strength_4h": trend_strength(indicator_4h),

        "ema_alignment": ema_alignment(indicator_15m),
    }


# ====================================================
# Chỉ cho phép BUY khi xu hướng tăng
# ====================================================

def allow_buy(result: Dict) -> bool:

    if not result["confirmed"]:
        return False

    if result["trend_4h"] != "UP":
        return False

    return True


# ====================================================
# Chỉ cho phép SELL khi xu hướng giảm
# ====================================================

def allow_sell(result: Dict) -> bool:

    if not result["confirmed"]:
        return False

    if result["trend_4h"] != "DOWN":
        return False

    return True