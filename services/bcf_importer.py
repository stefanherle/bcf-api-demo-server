import base64
import os
from bcf.bcfxml import load

from data import PROJECTS, TOPICS, COMMENTS, VIEWPOINTS
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
from datetime import datetime

from utils.converter import convert_xml_datetime


def import_bcf_folder(folder_path="data"):
    print(f"Lade BCF-Dateien aus: {folder_path}")

    for file in os.listdir(folder_path):
        if file.lower().endswith((".bcfzip", ".bcf")):
            full_path = os.path.join(folder_path, file)

            #  Dateiname ohne Endung
            file_name = os.path.splitext(file)[0]

            print(f"➡ Importiere {file}")

            import_bcfzip(full_path)


def import_bcfzip(file_path):
    # Projekt anlegen, falls nicht vorhanden
    

    with load(file_path) as bcf:
        project_guid = bcf.project.project_id
        if project_guid not in PROJECTS:
            PROJECTS[project_guid] = Project(
                guid=project_guid,
                name=bcf.project.name
            )

        for topic_guid, topic_handler in bcf.topics.items():
            topic = topic_handler.topic
            TOPICS[topic.guid] = Topic(
                guid=topic.guid,
                project_guid=project_guid,
                title=topic.title or "Untitled Topic",
                description=topic.description,
                creation_date=convert_xml_datetime(topic.creation_date) or datetime.utcnow()
            )

            for c in topic_handler.comments:
                COMMENTS[c.guid] = Comment(
                    guid=c.guid,
                    topic_guid=topic.guid,
                    comment=c.comment or "",
                    date=convert_xml_datetime(c.date) or datetime.utcnow(),
                    author=c.author
                )
            
            idx = 0
            for vp_guid, vi_handler in topic_handler.viewpoints.items():
                snapshot_bmp = vi_handler.snapshot
                visualization_info = vi_handler.visualization_info
                VIEWPOINTS[visualization_info.guid] = convert_viewpoint(topic.guid, idx, visualization_info, snapshot_bmp=snapshot_bmp)
                idx=idx+1


def convert_viewpoint(topic_guid, index, visualization_info, snapshot_bmp=None):
    snapshot = None
    if snapshot_bmp:
        snapshot = Snapshot(
            snapshot_type="png",
            snapshot_data=base64.b64encode(snapshot_bmp).decode("utf-8")
        )

    ortho = None
    if visualization_info.orthogonal_camera:
        oc = visualization_info.orthogonal_camera
        ortho = OrthogonalCamera(
            camera_view_point=oc.camera_view_point,
            camera_direction=oc.camera_direction,
            camera_up_vector=oc.camera_up_vector,
            view_to_world_scale=oc.view_to_world_scale
        )

    persp = None
    if visualization_info.perspective_camera:
        pc = visualization_info.perspective_camera
        persp = PerspectiveCamera(
            camera_view_point=pc.camera_view_point,
            camera_direction=pc.camera_direction,
            camera_up_vector=pc.camera_up_vector,
            field_of_view=pc.field_of_view
        )

    lines = [
        Line(start_point=l.start_point, end_point=l.end_point)
        for l in (visualization_info.lines.line or [])
    ]
    if len(lines) == 0:
        lines = None

    clipping = [
        ClippingPlane(location=cp.location, direction=cp.direction)
        for cp in (visualization_info.clipping_planes.clipping_plane or [])
    ]
    if len(clipping) == 0:
        clipping = None

    bitmaps = [
        Bitmap(
            bitmap_type=b.bitmap_type,
            bitmap_data=b.bitmap_data,
            location=b.location,
            normal=b.normal,
            up=b.up
        )
        for b in (visualization_info.bitmaps.bitmap or [])
    ]
    if len(bitmaps) == 0:
        bitmaps = None

    components = None
    if visualization_info.components:
        components = Components(
            selection=visualization_info.components.selection,
            coloring=visualization_info.components.coloring,
            visibility=visualization_info.components.visibility
        )

    return Viewpoint(
        guid=visualization_info.guid,
        topic_guid=topic_guid,
        index=index,
        orthogonal_camera=ortho,
        perspective_camera=persp,
        lines=lines,
        clipping_planes=clipping,
        bitmaps=bitmaps,
        snapshot=snapshot,
        components=components
    )
