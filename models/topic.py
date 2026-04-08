from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from utils.serializer import to_dict


@dataclass
class Topic:
    guid: str
    project_guid: str
    title: str
    description: Optional[str]
    creation_date: datetime

    def serialize(self):
        return to_dict(self)