from flask import Blueprint, jsonify
from bcf_api.components.repositories.data import TOPICS

bp = Blueprint("topics", __name__)


@bp.get("/topics")
def get_topics():
    return jsonify([t.serialize() for t in TOPICS.values()])


@bp.get("/topics/<topic_guid>")
def get_topic(topic_guid):
    topic = TOPICS.get(topic_guid)
    if not topic:
        return jsonify({"error": "Topic not found"})
    return jsonify(topic.serialize())


@bp.get("/projects/<project_guid>/topics")
def get_topics_for_project(project_guid):
    items = [
        t.serialize()
        for t in TOPICS.values()
        if t.project.guid == project_guid
    ]
    return jsonify(items)

@bp.get("/projects/<project_guid>/topics/<topic_guid>")
def get_topic_for_project(project_guid, topic_guid):
    topic = TOPICS.get(topic_guid)

    if not topic:
        return jsonify({"error": "Topic not found"})

    if topic.project.guid != project_guid:
        return jsonify({"error": "Topic does not belong to this project"})

    return jsonify(topic.serialize())