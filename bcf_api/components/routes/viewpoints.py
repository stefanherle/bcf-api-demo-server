import base64

from flask import Blueprint, Response, jsonify
from bcf_api.components.repositories.data import VIEWPOINTS, TOPICS

bp = Blueprint("viewpoints", __name__)


@bp.get("/viewpoints")
def get_viewpoints():
    return jsonify([
        v.serialize() for v in VIEWPOINTS.values()
    ])


@bp.get("/viewpoints/<viewpoint_guid>")
def get_viewpoint(viewpoint_guid):
    vp = VIEWPOINTS.get(viewpoint_guid)
    if not vp:
        return jsonify({"error": "Viewpoint not found"})
    return jsonify(vp.serialize())

@bp.get("/projects/<project_guid>/topics/<topic_guid>/viewpoints")
def get_viewpoints_for_project_topic(project_guid, topic_guid):
    topic = TOPICS.get(topic_guid)

    if not topic:
        return jsonify({"error": "Topic not found"})

    if topic.project.guid != project_guid:
        return jsonify({"error": "Topic does not belong to this project"})

    items = [vp.serialize() for vp in VIEWPOINTS.values() if vp.topic.guid == topic_guid]

    return jsonify(items)


@bp.get("/projects/<project_guid>/topics/<topic_guid>/viewpoints/<viewpoint_guid>")
def get_single_viewpoint_for_project_topic(project_guid, topic_guid, viewpoint_guid):
    topic = TOPICS.get(topic_guid)

    if not topic:
        return jsonify({"error": "Topic not found"})

    if topic.project.guid != project_guid:
        return jsonify({"error": "Topic does not belong to this project"})

    vp = VIEWPOINTS.get(viewpoint_guid)

    if not vp:
        return jsonify({"error": "Viewpoint not found"})

    if vp.topic.guid != topic_guid:
        return jsonify({"error": "Viewpoint does not belong to this topic"})

    return jsonify(vp.serialize())


@bp.get("/projects/<project_guid>/topics/<topic_guid>/viewpoints/<viewpoint_guid>/snapshot")
def get_snapshot(project_guid, topic_guid, viewpoint_guid):
    vp = VIEWPOINTS.get(viewpoint_guid)

    if not vp:
        return jsonify({"error": "Viewpoint not found"}), 404

    if vp.topic.guid != topic_guid:
        return jsonify({"error": "Viewpoint does not belong to this topic"}), 400

    if not vp.snapshot:
        return jsonify({"error": "No snapshot available"}), 404

    # Base64 → bytes
    try:
        img_bytes = base64.b64decode(vp.snapshot.snapshot_data)
    except Exception:
        return jsonify({"error": "Invalid snapshot data"}), 500

    # PNG direkt ausliefern
    return Response(img_bytes, mimetype="image/png")