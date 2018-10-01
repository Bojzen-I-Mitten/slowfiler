from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
db = SQLAlchemy(app)

app.config['SQLALCHEMY_BINDS'] = {
    'Dhomas': 'sqlite:////test.db'
}

# Import Blueprint modules.
from app.build.routes import mod_build


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error), 404

app.register_blueprint(mod_build)

db.create_all()
