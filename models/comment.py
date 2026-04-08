from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from utils.serializer import to_dict


@dataclass
class Comment:
    guid: str
    topic_guid: str
    comment: str
    date: datetime
    author: Optional[str] = None

    def serialize(self):
        return to_dict(self)