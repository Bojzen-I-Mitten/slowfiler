from flask import Blueprint, render_template, redirect, url_for, request, Response, flash
from sqlalchemy import desc, or_
from app import db, app
from werkzeug import secure_filename

from app.database.tables import Build



mod_build = Blueprint('data', __name__, url_prefix='/templates',
template_folder='templates')

@app.route('/')
def index():
    return render_template("index.html", build_data=Build.query.all())
