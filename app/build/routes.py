from flask import Blueprint, render_template, redirect, url_for, request, Response, flash
from sqlalchemy import desc, or_
from app import db, app
from werkzeug import secure_filename

from app.database.tables import Build



mod_build = Blueprint('data', __name__, url_prefix='/templates',
template_folder='templates')

@app.route('/compare/<int:buildnumber_one>&<int:buildnumber_two>')
def compare(buildnumber_one, buildnumber_two):
    build_data = Build.query.all()
    print(buildnumber_one)
    print(buildnumber_two)
    # make the database into a dict, build number being the key
    build_dict = {}
    for entry in build_data:
        if entry.build in build_dict:
            build_dict[entry.build].append(entry)
        else:
            build_dict[entry.build] = [entry]

    if (buildnumber_two in build_dict and buildnumber_one in build_dict):
        build_one = build_dict[buildnumber_one]
        build_two = build_dict[buildnumber_two]

        build_diff = {}
        for function in build_one:
            build_diff[function.name] = function.samples

        for function in build_two:
            if function.name in build_diff:
                build_diff[function.name] -= function.samples
            else:
                build_diff[function.name] = 0

        return render_template("compare.html", build_diff=build_diff)


    else:
        print("no beuno")

    difference = []

    return "Hej"



@app.route('/')
def index():
    build_data=Build.query.all()
    build_frame_time = {}

    # Crunch numbers from builds
    # Adds totalframe time and places it in a dict
    # Key is build number

    # make the database into a dict, build number being the key
    build_dict = {}
    for entry in build_data:
        if entry.build in build_dict:
            build_dict[entry.build].append(entry)
        else:
            build_dict[entry.build] = [entry]


    for build in build_data:
        if build.build in build_frame_time:
            build_frame_time[build.build] = build_frame_time[build.build] + build.samples
        else:
            build_frame_time[build.build] = build.samples


    return render_template("index.html", build_data=build_data,
                            build_frame_time=build_frame_time, last_build=build_dict[max(build_dict.keys())])
