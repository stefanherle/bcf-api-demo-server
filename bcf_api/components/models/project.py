from dataclasses import dataclass, field
from datetime import datetime
from bcf_api import config
from bcf_api.components.utils.serializer import to_dict


@dataclass
class Project:
    guid: str
    name: str
    filenames: list[str] = field(default_factory=list, metadata={"serialize": False})
    topics: list["Topic"] = field(default_factory=list, metadata={"shallow": True})

    def serialize(
        self,
        include_navigation_links=config.NAVI_LINKS,
        api_address=config.API_ADDRESS,
        relative_links=config.REL_URI
    ):
        data = to_dict(self)

        if include_navigation_links:
            prefix = f"{api_address.rstrip('/')}" if not relative_links else ""

            # Direkte Verbindung: Project → Topics
            data["topics@navigationLink"] = [
                f"{prefix}{config.API_PATH}/projects/{self.guid}/topics/{t.guid}"
                for t in self.topics
            ]

        return data
