from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
db = SQLAlchemy(app)

app.config['SQLALCHEMY_BINDS'] = {
    'Dhomas': 'sqlite:////test.db'
}


db.create_all(bind=['Dhomas'])


mod_missions = Blueprint('missions', __name__, url_prefix='/templates',
template_folder='templates')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error), 404

@app.route('/')
def index():
    return render_template('index.html')
