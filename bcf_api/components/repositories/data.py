from bcf_api.components.models.project import Project
from bcf_api.components.models.topic import Topic
from bcf_api.components.models.viewpoint import Viewpoint
from bcf_api.components.models.comment import Comment

# Globale In-Memory-Datenbanken
PROJECTS: dict[str, Project] = {}
TOPICS: dict[str, Topic] = {}
VIEWPOINTS: dict[str, Viewpoint] = {}
COMMENTS: dict[str, Comment] = {}