from dataclasses import dataclass, field
from typing import Optional, List

from bcf_api import config
from bcf_api.components.utils.serializer import to_dict


# ---------------------------------------------------------
# Camera Models
# ---------------------------------------------------------

@dataclass
class OrthogonalCamera:
    camera_view_point: List[float]
    camera_direction: List[float]
    camera_up_vector: List[float]
    view_to_world_scale: float


@dataclass
class PerspectiveCamera:
    camera_view_point: List[float]
    camera_direction: List[float]
    camera_up_vector: List[float]
    field_of_view: float


# ---------------------------------------------------------
# Geometry Models
# ---------------------------------------------------------

@dataclass
class Line:
    start_point: List[float]
    end_point: List[float]


@dataclass
class ClippingPlane:
    location: List[float]
    direction: List[float]


# ---------------------------------------------------------
# Bitmap Model
# ---------------------------------------------------------

@dataclass
class Bitmap:
    bitmap_type: str
    bitmap_data: str
    location: List[float]
    normal: List[float]
    up: List[float]


# ---------------------------------------------------------
# Snapshot Model
# ---------------------------------------------------------

@dataclass
class Snapshot:
    snapshot_type: str
    snapshot_data: str


# ---------------------------------------------------------
# Components Model
# ---------------------------------------------------------

@dataclass
class Components:
    selection: Optional[List[dict]] = None
    coloring: Optional[List[dict]] = None
    visibility: Optional[dict] = None


# ---------------------------------------------------------
# Viewpoint (Main Model)
# ---------------------------------------------------------

@dataclass
class Viewpoint:
    guid: str
    index: Optional[int] = None
    topic: "Topic" = field(default=None, metadata={"shallow": True})
    orthogonal_camera: "OrthogonalCamera" = None
    perspective_camera: "PerspectiveCamera" = None
    lines: list["Line"] = field(default_factory=list)
    clipping_planes: list["ClippingPlane"] = field(default_factory=list)
    bitmaps: list["Bitmap"] = field(default_factory=list)
    snapshot: "Snapshot" = None
    components: "Components" = None

    def serialize(
        self,
        include_navigation_links=config.NAVI_LINKS,
        api_address=config.API_ADDRESS,
        relative_links=config.REL_URI
    ):
        data = to_dict(self)

        if include_navigation_links:
            prefix = f"{api_address.rstrip('/')}" if not relative_links else ""

            data["topic@navigationLink"] = (
                f"{prefix}{config.API_PATH}/projects/{self.topic.project.guid}"
                f"/topics/{self.topic.guid}"
            )

            # Link zum Snapshot (falls vorhanden)
            if self.snapshot:
                data["snapshot@navigationLink"] = (
                    f"{prefix}{config.API_PATH}/projects/{self.topic.project.guid}"
                    f"/topics/{self.topic.guid}/viewpoints/{self.guid}/snapshot"
                )

        return data
