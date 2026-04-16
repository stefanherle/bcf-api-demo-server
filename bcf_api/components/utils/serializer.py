from dataclasses import is_dataclass, fields
from datetime import datetime

def to_dict(obj, seen=None):
    if obj is None:
        return None

    if seen is None:
        seen = set()

    # Zyklen verhindern
    if id(obj) in seen:
        return None
    seen.add(id(obj))

    # Dataclass
    if is_dataclass(obj):
        result = {}
        for f in fields(obj):
            # Felder mit serialize=False überspringen
            if f.metadata.get("serialize") is False:
                continue
            value = getattr(obj, f.name)

            # SHALLOW-Felder → nur GUID oder primitive Werte
            if f.metadata.get("shallow", False):
                if hasattr(value, "guid"):
                    result[f.name + "_guid"] = value.guid
                elif isinstance(value, list):
                    result[f.name] = [
                        v.guid for v in value if hasattr(v, "guid")
                    ]
                else:
                    result[f.name] = None
                continue

            # normale Felder → rekursiv
            result[f.name] = to_dict(value, seen)

        return result

    # Listen
    if isinstance(obj, list):
        return [to_dict(v, seen) for v in obj]

    # Dicts
    if isinstance(obj, dict):
        return {k: to_dict(v, seen) for k, v in obj.items()}

    # datetime
    if isinstance(obj, datetime):
        return obj.isoformat()

    # primitive Werte
    return obj
