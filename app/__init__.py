from flask import Flask
# from app import app

app = Flask(__name__)

from app.routes import routes