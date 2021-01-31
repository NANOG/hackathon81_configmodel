"""Configuration modeling API service."""

from flask import Flask

from configmodel.api.namespaces import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)
