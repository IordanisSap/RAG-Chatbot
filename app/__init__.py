from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__,
                    static_url_path='', 
                    static_folder='static',
                )

    app.register_blueprint(main)

    return app