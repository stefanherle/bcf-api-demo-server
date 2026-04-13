from flask import Blueprint, jsonify
from bcf_api.components.repositories.data import PROJECTS

bp = Blueprint("projects", __name__)


@bp.get("/projects")
def get_projects():
    return jsonify([p.serialize() for p in PROJECTS.values()])


@bp.get("/projects/<project_guid>")
def get_project(project_guid):
    project = PROJECTS.get(project_guid)
    if not project:
        return jsonify({"error": "Project not found"})
    return jsonify(project.serialize())
