from datetime import datetime, timezone, timedelta


def datetime_now_moscow():
    return datetime.now(timezone(timedelta(hours=3)))


def set_moscow_timezone(dt: datetime) -> datetime:
    moscow_tz = timezone(timedelta(hours=3))
    if dt.tzinfo is None:
        return dt.replace(tzinfo=moscow_tz)
    else:
        return dt.astimezone(moscow_tz)

