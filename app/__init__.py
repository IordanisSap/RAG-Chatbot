from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__,
                    static_url_path='', 
                    static_folder='static',
                )
    app.secret_key = "super secret key"
    app.register_blueprint(main)

    return app