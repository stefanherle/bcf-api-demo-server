from flask import Flask
from routes.projects import bp as projects_bp
from routes.topics import bp as topics_bp
from routes.viewpoints import bp as viewpoints_bp
from routes.comments import bp as comments_bp


from services.bcf_importer import import_bcf_folder


def create_app():
    app = Flask(__name__)  

    app.register_blueprint(projects_bp, url_prefix="/bcf/3.0")
    app.register_blueprint(topics_bp, url_prefix="/bcf/3.0")
    app.register_blueprint(viewpoints_bp, url_prefix="/bcf/3.0")
    app.register_blueprint(comments_bp, url_prefix="/bcf/3.0")

    @app.get("/bcf/3.0")
    def root():
        return {
            "version": "3.0",
            "resources": {
                "projects": "/bcf/3.0/projects",
                "topics": "/bcf/3.0/topics",
                "viewpoints": "/bcf/3.0/viewpoints",
                "comments": "/bcf/3.0/comments"
            }
        }
    
    # BCF-Dateien beim Start laden
    import_bcf_folder("data")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
