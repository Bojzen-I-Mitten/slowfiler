from flask import Blueprint, render_template, redirect, url_for, request, Response, flash
from sqlalchemy import desc, or_
from app import db, app
from werkzeug import secure_filename
import os
import time
from app.database.tables import Function_build, Build_data, Build_fps

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
    Function_build.query.delete()
    Build_data.query.delete()
    time.sleep(0.5)
    db.session.commit()

    return redirect(url_for("builds"))

@app.route('/builds/compare/', methods = ['POST', 'GET'])
def compare():
    build_data = Function_build.query.all()

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
    function_build_data = Function_build.query.all()
    build_data = Build_data.query.all()
    fps_samples = Build_fps.query.all()

    sorted_fps_samples = {}
    for sample in fps_samples:
        if sample.build not in sorted_fps_samples:
            sorted_fps_samples[sample.build] = [sample.sample]
        else:
            sorted_fps_samples[sample.build].append(sample.sample)

    if (len(build_data) < 1 and len(function_build_data) < 1):
        runTestsAndUploadResultsToDb()
        function_build_data = Function_build.query.all()
        build_data = Build_data.query.all()
    # Convert build_data into a dict, where ID is the key

    build_data_sorted = {}
    for function in function_build_data:
        if function.build not in build_data_sorted:
            build_data_sorted[function.build] = [function]
        else:
            build_data_sorted[function.build].append(function)

    return render_template("dashboard.html",  build_data_sorted = build_data_sorted,
        build_data = build_data, sorted_fps_samples = sorted_fps_samples)
