from dataclasses import dataclass

from utils.serializer import to_dict


@dataclass
class Project:
    guid: str
    name: str

    def serialize(self):
        return to_dict(self)