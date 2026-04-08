from flask import Blueprint, jsonify
from data import COMMENTS, TOPICS

bp = Blueprint("comments", __name__)


@bp.get("/topics/<topic_guid>/comments")
def get_comments(topic_guid):
    return jsonify([
        c.serialize() for c in COMMENTS.values()
        if c.topic_guid == topic_guid
    ])


@bp.get("/comments/<comment_guid>")
def get_comment(comment_guid):
    c = COMMENTS.get(comment_guid)
    if not c:
        return jsonify({"error": "Comment not found"})
    return jsonify(c.serialize())


@bp.get("/projects/<project_guid>/topics/<topic_guid>/comments")
def get_comments_for_project_topic(project_guid, topic_guid):
    topic = TOPICS.get(topic_guid)

    if not topic:
        return jsonify({"error": "Topic not found"})

    if topic.project_guid != project_guid:
        return jsonify({"error": "Topic does not belong to this project"})

    items = [
        c.serialize()
        for c in COMMENTS.values()
        if c.topic_guid == topic_guid
    ]

    return jsonify(items)


@bp.get("/projects/<project_guid>/topics/<topic_guid>/comments/<comment_guid>")
def get_single_comment_for_project_topic(project_guid, topic_guid, comment_guid):
    topic = TOPICS.get(topic_guid)

    if not topic:
        return jsonify({"error": "Topic not found"})

    if topic.project_guid != project_guid:
        return jsonify({"error": "Topic does not belong to this project"})

    c = COMMENTS.get(comment_guid)

    if not c:
        return jsonify({"error": "Comment not found"})

    if c.topic_guid != topic_guid:
        return jsonify({"error": "Comment does not belong to this topic"})

    return jsonify(c.serialize())