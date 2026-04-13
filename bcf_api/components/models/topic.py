from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

from bcf_api import config
from bcf_api.components.utils.serializer import to_dict


@dataclass
class Topic:

    # Required laut Schema
    guid: str
    server_assigned_id: str
    title: str
    creation_date: datetime
    creation_author: str

    # Optionale Felder aus dem Schema
    topic_type: Optional[str] = None
    topic_status: Optional[str] = None
    reference_links: Optional[List[str]] = None
    priority: Optional[str] = None
    labels: Optional[List[str]] = None
    modified_date: Optional[datetime] = None
    modified_author: Optional[str] = None
    assigned_to: Optional[str] = None
    stage: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    
    project: "Project" = field(default=None, metadata={"shallow": True})
    viewpoints: List["Viewpoint"] = field(default_factory=list, metadata={"shallow": True})
    comments: List["Comment"] = field(default_factory=list, metadata={"shallow": True})

    def serialize(
        self,
        include_navigation_links=config.NAVI_LINKS,
        api_address=config.API_ADDRESS,
        relative_links=config.REL_URI
    ):
        data = to_dict(self)

        if include_navigation_links:
            prefix = f"{api_address.rstrip('/')}" if not relative_links else ""

            data["project@navigationLink"] = (
                f"{prefix}{config.API_PATH}/projects/{self.project.guid}"
            )

            data["viewpoints@navigationLink"] = [
                f"{prefix}{config.API_PATH}/projects/{self.project.guid}/topics/{self.guid}/viewpoints/{v.guid}"
                for v in self.viewpoints
            ]

            data["comments@navigationLink"] = [
                f"{prefix}{config.API_PATH}/projects/{self.project.guid}/topics/{self.guid}/comments/{c.guid}"
                for c in self.comments
            ]

        return data