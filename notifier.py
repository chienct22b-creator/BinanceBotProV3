"""
====================================================
BinanceBotProV3
Notifier Engine
====================================================
"""

from datetime import datetime, timedelta


# ==================================================
# Thời gian cooldown
# ==================================================

DEFAULT_COOLDOWN = 120      # phút


# ==================================================
# Bộ nhớ
# ==================================================

_last_alert = {}


# ==================================================
# Tạo key riêng
# ==================================================

def make_key(symbol, timeframe):

    return f"{symbol}_{timeframe}"


# ==================================================
# Kiểm tra cooldown
# ==================================================

def cooldown_expired(last_time, cooldown):

    return datetime.now() >= last_time + timedelta(minutes=cooldown)


# ==================================================
# Có được gửi không
# ==================================================

def should_notify(

    symbol,

    timeframe,

    direction,

    score,

    cooldown=DEFAULT_COOLDOWN

):

    key = make_key(symbol, timeframe)

    now = datetime.now()

    if key not in _last_alert:

        _last_alert[key] = {

            "direction": direction,

            "score": score,

            "time": now

        }

        return True

    info = _last_alert[key]

    # Đổi BUY -> SELL
    if info["direction"] != direction:

        _last_alert[key] = {

            "direction": direction,

            "score": score,

            "time": now

        }

        return True

    # Cooldown
    if cooldown_expired(

        info["time"],

        cooldown

    ):

        _last_alert[key] = {

            "direction": direction,

            "score": score,

            "time": now

        }

        return True

    return False


# ==================================================
# Xóa coin khỏi bộ nhớ
# ==================================================

def reset_symbol(symbol):

    delete_keys = []

    for key in _last_alert:

        if key.startswith(symbol):

            delete_keys.append(key)

    for key in delete_keys:

        del _last_alert[key]


# ==================================================
# Xóa toàn bộ
# ==================================================

def reset_all():

    _last_alert.clear()


# ==================================================
# Lấy thông tin cuối
# ==================================================

def last_alert(symbol, timeframe):

    key = make_key(symbol, timeframe)

    return _last_alert.get(key)


# ==================================================
# Thống kê
# ==================================================

def notifier_status():

    return {

        "tracked_symbols": len(_last_alert),

        "symbols": list(_last_alert.keys())

    }