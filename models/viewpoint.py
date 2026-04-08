from dataclasses import dataclass
from typing import Optional, List

from utils.serializer import to_dict


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
    topic_guid: str
    index: Optional[int] = None
    orthogonal_camera: Optional[OrthogonalCamera] = None
    perspective_camera: Optional[PerspectiveCamera] = None
    lines: Optional[List[Line]] = None
    clipping_planes: Optional[List[ClippingPlane]] = None
    bitmaps: Optional[List[Bitmap]] = None
    snapshot: Optional[Snapshot] = None
    components: Optional[Components] = None

    def serialize(self):
        return to_dict(self)
