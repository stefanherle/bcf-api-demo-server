from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from bcf_api import config
from bcf_api.components.models.topic import Topic
from bcf_api.components.models.viewpoint import Viewpoint
from bcf_api.components.utils.serializer import to_dict


@dataclass
class Comment:
    guid: str
    date: datetime
    author: str
    comment: str

    # Optionale Felder laut comment_GET.json
    modified_date: Optional[datetime] = None
    modified_author: Optional[str] = None
    
    topic: Topic | None = field(default=None, metadata={"shallow": True})
    viewpoint: Viewpoint | None = field(default=None, metadata={"shallow": True})
    

    def serialize(
        self,
        include_navigation_links=config.NAVI_LINKS,
        api_address=config.API_ADDRESS,
        relative_links=config.REL_URI
    ):
        data = to_dict(self)

        if include_navigation_links:
            prefix = f"{api_address.rstrip('/')}" if not relative_links else ""

            # Nur direkte Verbindung: Comment → Topic
            data["topic@navigationLink"] = (
                f"{prefix}{config.API_PATH}/projects/{self.topic.project.guid}"
                f"/topics/{self.topic.guid}"
            )
            if self.viewpoint is not None:
                data["viewpoint@navigationLink"] = (
                    f"{prefix}{config.API_PATH}/projects/{self.topic.project.guid}"
                    f"/topics/{self.topic.guid}/viewpoints/{self.viewpoint.guid}"
                )

        return data


        