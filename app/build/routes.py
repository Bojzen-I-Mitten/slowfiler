from flask import Blueprint, render_template, redirect, url_for, request, Response, flash
from sqlalchemy import desc, or_
from app import db, app
from werkzeug import secure_filename
import os
import time
from app.database.tables import Build, Build_time

from handleData import runTestsAndUploadResultsToDb

mod_build = Blueprint('data', __name__, url_prefix='/builds/',
template_folder='templates')

@app.route('/builds/runtests/')
def runtest():
    print("Starting thomas")
    os.system("run.exe.lnk")
    print("Starting crunch of data")
    results = runTestsAndUploadResultsToDb()
    print("All done, now showing page")
    return redirect(url_for("builds"))


@app.route('/builds/nukedatabase/')
def nukedatabase():
    Build.query.delete()
    Build_time.query.delete()
    time.sleep(0.5)
    db.session.commit()

    return redirect(url_for("builds"))

@app.route('/builds/compare/', methods = ['POST', 'GET'])
def compare():
    build_data = Build.query.all()

    # Get all build id's in the list
    builds = [function.build for function in build_data]
    # Only keep one instance of the build id's
    builds = list(set(builds))

    build_dict = {}

    if request.method == 'POST':
        buildnumber_one = int(request.form['sel1'])
        buildnumber_two = int(request.form['sel2'])

        for entry in build_data:
            if entry.build in build_dict:
                build_dict[entry.build].append(entry)
            else:
                build_dict[entry.build] = [entry]

        print(build_dict[buildnumber_two])
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

            return render_template("compare.html", build_diff=build_diff, builds=builds)


    return render_template("compare.html", builds=builds, build_diff=build_dict)


@app.route('/builds/')
def builds():
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


    last_build=[]
    if  not not build_dict.keys():
        last_build=build_dict[max(build_dict.keys())]


    build_time = Build_time.query.all()
    return render_template("dashboard.html", build_data=build_data,
                            build_frame_time=build_frame_time,
                            last_build=last_build,
                            build_time=build_time)
