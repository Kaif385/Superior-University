from flask import Flask

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

from app import routes
