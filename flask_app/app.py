# flask_app/app.py

from flask import Flask
from routes.health import health_bp
from routes.jobs import jobs_bp
from routes.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__,template_folder="templates", static_folder="static")
    

    # enregistrer les routes
    app.register_blueprint(health_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(dashboard_bp)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)
