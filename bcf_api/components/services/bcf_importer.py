import base64
import os
from datetime import datetime
import logging
import uuid
from bcf.bcfxml import load

from bcf_api.components.repositories.data import PROJECTS, TOPICS, COMMENTS, VIEWPOINTS
from bcf_api.components.models.project import Project
from bcf_api.components.models.topic import File, Topic
from bcf_api.components.models.comment import Comment
from bcf_api.components.models.viewpoint import (
    Viewpoint,
    OrthogonalCamera,
    PerspectiveCamera,
    Line,
    ClippingPlane,
    Bitmap,
    Snapshot,
    Components
)

from bcf_api.components.utils.converter import convert_xml_datetime

logger = logging.getLogger()


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
    try:
        with load(file_path) as bcf:
            return import_bcfzip_loaded(bcf, file_path)
    except Exception as e:
        logger.error(f"Fehler beim Laden von {file_path}: {e}")


def import_bcfzip_loaded(bcf, file_path):
    project_guid = bcf.project.project_id if bcf.project is not None else str(uuid.uuid1())
    project_name = bcf.project.name if bcf.project is not None else file_path.replace(" ", "")
    filename = os.path.basename(file_path)
    if project_guid not in PROJECTS:
        PROJECTS[project_guid] = Project(
            guid=project_guid,
            name=project_name,
            filenames=[filename]
        )
    elif filename not in PROJECTS[project_guid].filenames:
        PROJECTS[project_guid].filenames.append(filename)

    for topic_guid, topic_handler in bcf.topics.items():
        topic = topic_handler.topic
        TOPICS[topic.guid] = Topic(
            guid=topic.guid,
            server_assigned_id=topic.server_assigned_id,
            title=topic.title or "Untitled Topic",
            creation_date=convert_xml_datetime(topic.creation_date) or datetime.utcnow(),
            creation_author=topic.creation_author,

            topic_type=topic.topic_type,
            topic_status=topic.topic_status,
            reference_links=topic.reference_links,
            priority=topic.priority or None,
            labels=topic.labels,
            modified_date=convert_xml_datetime(topic.modified_date) or datetime.utcnow(),
            modified_author=topic.modified_author,
            assigned_to=topic.assigned_to,
            stage=topic.stage,
            description=topic.description,
            due_date=convert_xml_datetime(topic.due_date) or None,

            project=PROJECTS[project_guid],
        )
        PROJECTS[project_guid].topics.append(TOPICS[topic.guid])
        
        for file in topic_handler.header.files.file:
            new_file = File(
                filename=file.filename,
                date=convert_xml_datetime(file.date),
                reference=file.reference,
                ifc_project=file.ifc_project,
                ifc_spatial_structure_element=file.ifc_spatial_structure_element,
                is_external=file.is_external
            )
            TOPICS[topic.guid].files.append(new_file)

        idx = 0
        for vp_guid, vi_handler in topic_handler.viewpoints.items():
            snapshot_bmp = vi_handler.snapshot
            visualization_info = vi_handler.visualization_info
            VIEWPOINTS[visualization_info.guid] = convert_viewpoint(topic.guid, idx, visualization_info, snapshot_bmp=snapshot_bmp)
            TOPICS[topic.guid].viewpoints.append(VIEWPOINTS[visualization_info.guid])
            idx=idx+1

        for c in topic_handler.comments:
            COMMENTS[c.guid] = Comment(
                guid=c.guid,
                date=convert_xml_datetime(c.date) or datetime.utcnow(),
                author=c.author,
                comment=c.comment or "",
                modified_date=convert_xml_datetime(c.modified_date) or None,
                modified_author=c.modified_author or None,
                topic=TOPICS[topic.guid],
                viewpoint=VIEWPOINTS[c.viewpoint.guid] or None
            )
            TOPICS[topic.guid].comments.append(COMMENTS[c.guid])
            
            


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
        topic=TOPICS[topic_guid],
        index=index,
        orthogonal_camera=ortho,
        perspective_camera=persp,
        lines=lines,
        clipping_planes=clipping,
        bitmaps=bitmaps,
        snapshot=snapshot,
        components=components
    )
