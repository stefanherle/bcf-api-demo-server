from datetime import datetime

from models.project import Project
from models.topic import Topic
from models.comment import Comment
from models.viewpoint import (
    Viewpoint,
    OrthogonalCamera,
    PerspectiveCamera,
    Line,
    ClippingPlane,
    Bitmap,
    Snapshot,
    Components
)

# ---------------------------------------------------------
# Projects
# ---------------------------------------------------------

PROJECTS = {
    "p1": Project(
        guid="p1",
        name="Demo Project"
    )
}

# ---------------------------------------------------------
# Topics
# ---------------------------------------------------------

TOPICS = {
    "t1": Topic(
        guid="t1",
        project_guid="p1",
        title="Collision detected",
        description="Two pipes intersect",
        creation_date=datetime.utcnow()
    )
}

# ---------------------------------------------------------
# Viewpoints
# ---------------------------------------------------------

VIEWPOINTS = {
    "v1": Viewpoint(
        guid="v1",
        topic_guid="t1",
        index=1,
        orthogonal_camera=OrthogonalCamera(
            camera_view_point=[10, 5, 3],
            camera_direction=[0, 0, -1],
            camera_up_vector=[0, 1, 0],
            view_to_world_scale=1.0
        ),
        perspective_camera=None,
        lines=[
            Line(start_point=[0, 0, 0], end_point=[1, 1, 1])
        ],
        clipping_planes=[
            ClippingPlane(location=[0, 0, 1], direction=[0, 0, -1])
        ],
        bitmaps=[],
        snapshot=Snapshot(
            snapshot_type="png",
            snapshot_data="<base64>"
        ),
        components=Components(
            selection=[],
            coloring=[],
            visibility={"default_visibility": True, "exceptions": []}
        )
    )
}

# ---------------------------------------------------------
# Comments
# ---------------------------------------------------------

COMMENTS = {
    "c1": Comment(
        guid="c1",
        topic_guid="t1",
        comment="Please fix this issue",
        date=datetime.utcnow(),
        author="John Doe"
    )
}
