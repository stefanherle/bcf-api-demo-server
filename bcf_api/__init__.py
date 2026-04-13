import os

from flask import Flask
from flask_cors import CORS
from bcf_api import config
from bcf_api.components.routes.projects import bp as projects_bp
from bcf_api.components.routes.topics import bp as topics_bp
from bcf_api.components.routes.viewpoints import bp as viewpoints_bp
from bcf_api.components.routes.comments import bp as comments_bp


from bcf_api.components.services.bcf_importer import import_bcf_folder


def create_app(serving_path=os.path.join(os.path.dirname(__file__), "data"), config_path=os.path.join(os.path.dirname(__file__), "config.py")):
    app = Flask(__name__)  
    CORS(app)
    app.config.from_pyfile(config_path)

    app.register_blueprint(projects_bp, url_prefix=config.API_PATH)
    app.register_blueprint(topics_bp, url_prefix=config.API_PATH)
    app.register_blueprint(viewpoints_bp, url_prefix=config.API_PATH)
    app.register_blueprint(comments_bp, url_prefix=config.API_PATH)

    @app.get(config.API_PATH)
    def root():

        prefix = f"{config.API_ADDRESS.rstrip('/')}" if not config.REL_URI else ""

        return {
            "version": "3.0",
            "resources": {
                "projects@navigationLink": f"{prefix}{config.API_PATH}/projects",
                "topics@navigationLink": f"{prefix}{config.API_PATH}/topics",
                "viewpoints@navigationLink": f"{prefix}{config.API_PATH}/viewpoints",
                "comments@navigationLink": f"{prefix}{config.API_PATH}/comments"
            }
        }
    
    # BCF-Dateien beim Start laden
    import_bcf_folder(serving_path)

    return app

