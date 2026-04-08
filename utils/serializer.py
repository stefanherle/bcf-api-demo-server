from dataclasses import is_dataclass, asdict
from datetime import datetime

def to_dict(obj):
    if obj is None:
        return None

    # Dataclass → dict
    if is_dataclass(obj):
        data = {}
        for key, value in asdict(obj).items():
            if value is not None:
                data[key] = to_dict(value)
        return data

    # Liste → rekursiv serialisieren
    if isinstance(obj, list):
        return [to_dict(v) for v in obj if v is not None]

    # Dict → rekursiv serialisieren
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items() if v is not None}

    # Primitive Werte
    if isinstance(obj, datetime):
        return obj.isoformat()

    return obj
