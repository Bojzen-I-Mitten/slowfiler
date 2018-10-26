import re
import sqlite3
import os
from discord_hooks import Webhook

import json
import statistics

import jenkins


def runTestsAndUploadResultsToDb():
    functionDict = {}
    try:
        with open("data.json", "r") as ins:
            data = json.load(ins)

        function_data = {}
        for function in data["SlowfilerData"]["functions"]:
            rawData = data["SlowfilerData"]["functions"][function] # Gives an array of all samples
            function_data[function] = {}
            function_data[function]["avg"] = sum(rawData) / len(rawData)
            function_data[function]["std"] = statistics.stdev(rawData)
            function_data[function]["max"] = max(rawData)
            function_data[function]["min"] = min(rawData)


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

        for function in function_data: # For every function, send data to database
            try:
                table_name = 'Function_build'
                column_name = 'function_name'
                column_avg = 'avg'
                column_std = 'std'
                column_max = 'max'
                column_min = 'min'
                column_build = 'build'

                sample = function_data[function]

                c.execute("INSERT INTO {tn} ({cn}, {ca}, {cs}, {cm}, {cnv}, {cb}) VALUES (\"{vn}\", {va}, {vs}, {vm}, {vnv}, {vb})".\
                    format(tn=table_name, cn=column_name, ca=column_avg, cs=column_std,
                        cm=column_max, cnv=column_min, cb=column_build,
                        vn=function, va=(sample["avg"]), vs=sample["std"], vm=sample["max"], vnv=sample["min"], vb=build_number))

            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

        try:
            table_name = 'Build_time'
            column_name = 'build_number'
            column_duration = 'build_duration'
            c.execute(("INSERT INTO {tn} ({cn}, {cd}) VALUES ({v1}, {v2})").\
                format(tn=table_name, cn=column_name, cd=column_duration, v1=build_number, v2=build_duration))
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

        # Close connection
        conn.commit()
        conn.close()

        url = 'https://discordapp.com/api/webhooks/489031312032923649/m_DPPOX33J1unuGYKHnHYtEID2qkYmKYNj5yEjajmfc0yxnT0iwm69k18fz6rE8DsRcD'


        embed = Webhook(url, color=428644)

        embed.set_author(name='Slowfiler', icon='https://i.imgur.com/rdm3W9t.png')
        embed.set_desc('New preformance report available at http://192.168.1.141:8069/builds/ ')
        embed.set_thumbnail('https://t4.rbxcdn.com/fee318796364847e0ff53ea658490477')
        embed.set_image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxGPybbkwZhiYyED4lUqxkYJLw2YGQ95viN9vRRNpe7zvbBX2b-g')
        embed.set_footer(text='Slowfiler, copyright 3-D asset', ts=True)

        #embed.post()


        return 0
        #try:
        #    os.rename("data.csv", str(job["lastBuild"]["number"]) + ".csv")
    except IOError:
        print("Could not open file")
        return -1
