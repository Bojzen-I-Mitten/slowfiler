import re
import sqlite3
import os
from discord_hooks import Webhook
from hookurl import url
import json
import numpy as np
import statistics

import jenkins


def runTestsAndUploadResultsToDb(gameReturn, EditorReturn):
    functionDict = {}
    if (not gameReturn and not EditorReturn):
        try:
            with open("C:\\Program Files (x86)\\Jenkins\\workspace\\SSP\\thomas\\CompiledGame\\Bin\\data.json", "r") as ins:
                data = json.load(ins)

            function_data = {}
            for processor_id in data["SlowfilerData"]["processor"]:
                for function in data["SlowfilerData"]["processor"][processor_id]["functions"]:
                    rawData = [int(s) for s in data["SlowfilerData"]["processor"][processor_id]["functions"][function].split(',')];
                    rawData = [x / 1000000.0 for x in rawData] # Gives an array of all samples
                    function_data[function] = {}
                    function_data[function]["avg"] = sum(rawData) / len(rawData)

                    try:
                        function_data[function]["std"] = statistics.stdev(rawData)
                    except statistics.StatisticsError:
                        print("Only one entry for {}, cannot calculate varience".format(function))
                        function_data[function]["std"] = 0

                    function_data[function]["max"] = max(rawData)
                    function_data[function]["min"] = min(rawData)
                    array = np.array(rawData);
                    function_data[function]["97th"] = np.percentile(array, 97)
            # parse all fps samples from json object
            fps_samples_cpu = [x / 1000000 for x in data["SlowfilerData"]["build"]["fps"][::10]]
            fps_samples_gpu = [x / 1000000 for x in data["SlowfilerData"]["gpu"][::10]]

            # fetch all jenkins data
            # We are going to assume that we have the data of the latest job
            j = jenkins.Jenkins("http://192.168.1.141:8080", "admin", "jenkinsjenkar")
            job =  j.get_job_info("SSP") # All info from job SSP
            build_number = job["lastBuild"]["number"] #
            build_duration = j.get_build_info("SSP", job["lastBuild"]["number"])["duration"] # Fetch duration of latest build


            # Connect to database
            sqlite_file = 'C:\\test.db'
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()

            for sample in fps_samples_cpu: # For every function, send data to database
                try:
                    table_name = 'Build_fps_gpu'
                    column_sample = 'sample'
                    column_build = 'build'
                    c.execute("INSERT INTO {tn} ({cs}, {cb}) VALUES ({vs}, {vb})".\
                        format(tn=table_name, cs=column_sample, cb=column_build, vs=sample, vb=build_number))

                except sqlite3.IntegrityError:
                    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

            for sample in fps_samples_gpu: # For every function, send data to database
                try:
                    table_name = 'Build_fps_cpu'
                    column_sample = 'sample'
                    column_build = 'build'
                    c.execute("INSERT INTO {tn} ({cs}, {cb}) VALUES ({vs}, {vb})".\
                        format(tn=table_name, cs=column_sample, cb=column_build, vs=sample, vb=build_number))

                except sqlite3.IntegrityError:
                    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

            for function in function_data: # For every function, send data to database
                try:
                    table_name = 'Function_build'
                    column_name = 'function_name'
                    column_avg = 'avg'
                    column_std = 'std'
                    column_max = 'max'
                    column_min = 'min'
                    column_build = 'build'
                    column_97th = 'p97th'

                    sample = function_data[function]

                    c.execute("INSERT INTO {tn} ({cn}, {ca}, {cs}, {cm}, {cnv}, {cb}, {c97}) VALUES (\"{vn}\", {va}, {vs}, {vm}, {vnv}, {vb}, {v97})".\
                        format(tn=table_name, cn=column_name, ca=column_avg, cs=column_std,
                            cm=column_max, cnv=column_min, cb=column_build, c97=column_97th,
                            vn=function, va=(sample["avg"]), vs=sample["std"], vm=sample["max"], vnv=sample["min"], vb=build_number, v97=sample["97th"]))

                except sqlite3.IntegrityError:
                    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

            try:
                table_name = 'Build_data'
                column_number = "build_number"
                column_duration = "build_time_duration"
                column_ramusage = "build_ramusage"
                column_vramuasge = "build_vramusage"
                column_avgfps = "build_avgfps"
                column_minfps = "build_minfps"
                column_stdfps = "build_stdfps"


                c.execute("INSERT INTO {tn} ({cn}, {cd}, {cr}, {cv}, {cavgfps}, {cminfps}, {cstdfps}) VALUES ({vn}, {vd}, {vr}, {vv}, {vavgfps}, {vminfps}, {vstdfps})".\
                    format(tn=table_name, cn=column_number, cd=column_duration,
                            cr=column_ramusage, cv=column_vramuasge, cavgfps=column_avgfps,
                            cminfps=column_minfps, cstdfps=column_stdfps,
                            vn=build_number, vd=build_duration, vr=data["SlowfilerData"]["build"]["ramUsage"],
                            vv=data["SlowfilerData"]["build"]["vramUsage"],
                            vavgfps=sum(fps_samples_cpu) / len(fps_samples_cpu), vminfps=min(fps_samples_cpu),
                            vstdfps=statistics.stdev(fps_samples_cpu)))

            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))
            # Close connection
            conn.commit()
            conn.close()


            embed = Webhook(url, color=428644)
            ram_usage = data["SlowfilerData"]["build"]["ramUsage"]
            vram_usage = data["SlowfilerData"]["build"]["vramUsage"]
            avg_fps = sum(fps_samples_cpu) / len(fps_samples_cpu)
            embed.set_author(name='Slowfiler', icon='https://i.imgur.com/rdm3W9t.png')
            embed.set_desc('New preformance report available at http://192.168.1.141:8069/builds/ ')
            embed.add_field(name='Average frametime:',value="{} ms".format(avg_fps))
            embed.add_field(name='RAM USAGE:',value="{} mb".format(ram_usage - vram_usage))
            embed.add_field(name='VRAM USAGE:',value="{} mb".format(vram_usage))

            if (ram_usage - vram_usage) < 256 and vram_usage < 512 and avg_fps < 32:
                embed.add_field(name='STATUS:',value="PASS")
            else:
                embed.add_field(name='STATUS:',value="FAIL")

            embed.set_thumbnail('https://t4.rbxcdn.com/fee318796364847e0ff53ea658490477')
            embed.set_footer(text='Slowfiler, copyright 3-D asset', ts=True)

            embed.post()

            return 0
        except IOError:
            print("Could not open file")
            return -1
    else:
        embed = Webhook(url, color=428644)
        embed.set_author(name='Slowfiler', icon='https://i.imgur.com/rdm3W9t.png')
        embed.set_desc('Could not run game or editor ')
        if (not gameReturn):
            embed.add_field(name='GAME STATUS:',value="FAIL")
        if (not EditorReturn):
            embed.add_field(name='EDITOR STATUS:',value="FAIL")
        embed.set_thumbnail('https://t4.rbxcdn.com/fee318796364847e0ff53ea658490477')
        embed.set_footer(text='Slowfiler, copyright 3-D asset', ts=True)

        embed.post()
        return -1
