from flask import Flask
from flask_cors import CORS


def create_app():
    """ Creates an instance of the Flask app """
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.url_map.strict_slashes = False

    from .routes import verification_routes
    app.register_blueprint(verification_routes, url_prefix='/api')
    return app
