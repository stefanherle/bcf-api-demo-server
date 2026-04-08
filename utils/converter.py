from datetime import datetime

def convert_xml_datetime(value):
    
    if isinstance(value, datetime):
        return value

    if hasattr(value, "year") and hasattr(value, "month") and hasattr(value, "day"):
        try:
            return datetime(
                value.year,
                value.month,
                value.day,
                getattr(value, "hour", 0),
                getattr(value, "minute", 0),
                getattr(value, "second", 0),
                getattr(value, "microsecond", 0),
                tzinfo=None
            )
        except Exception:
            pass

    return value
