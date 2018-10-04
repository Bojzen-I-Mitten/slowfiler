import re
import sqlite3
import os
from discord_hooks import Webhook

import jenkins


def runTestsAndUploadResultsToDb():
    functionDict = {}
    try:
        with open("C:\\Program Files (x86)\\Jenkins\\workspace\\SSP\\thomas\\DebugEditorBuild64\\data.csv", "r") as ins:
            for line in ins:
                functionName = re.match('[^0-9]*', line).group(0).split(" ")[-2]
                functionName = "::".join(functionName.split("::")[-2:])
                #functionName = functionName.replace("::", "")
                functionName = functionName.split("(", 1)[0]
                line = line.split(" ")[5:]
                line = line[:-1]
                line = [int(i) for i in line]

                functionDict[functionName] = line

        outliers = {}
        graph_data = []


        for functionName in functionDict:
            average_frame_time = (functionName, sum(functionDict[functionName]) / len(functionDict[functionName]),
            max(functionDict[functionName]), min(functionDict[functionName]))
            graph_data.append(average_frame_time)



        sqlite_file = 'C:\\test.db'

        # fetch all jenkins data
        # We are going to assume that we have the data of the latest job
        j = jenkins.Jenkins("http://127.0.0.1:8080", "admin", "jenkinsjenkar")
        job =  j.get_job_info("SSP") # All info from job SSP
        build_number = job["lastBuild"]["number"] #
        build_duration = j.get_build_info("SSP", job["lastBuild"]["number"])["duration"] # Fetch duration of latest build
        print(build_number)

        url = 'https://discordapp.com/api/webhooks/489031312032923649/m_DPPOX33J1unuGYKHnHYtEID2qkYmKYNj5yEjajmfc0yxnT0iwm69k18fz6rE8DsRcD'


        embed = Webhook(url, color=428644)

        embed.set_author(name='Slowfiler', icon='https://i.imgur.com/rdm3W9t.png')
        embed.set_desc('New data published at http://192.168.1.141:8069/builds/ \U0001f603 ')
        embed.set_thumbnail('https://t4.rbxcdn.com/fee318796364847e0ff53ea658490477')
        embed.set_image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxGPybbkwZhiYyED4lUqxkYJLw2YGQ95viN9vRRNpe7zvbBX2b-g')
        embed.set_footer(text='Here is my footer text', ts=True)

        embed.post()

        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        for data_point in graph_data: # For every function, send data to database
            try:
                table_name = 'Build'
                column_name = 'name'
                column_sample = 'samples'
                column_build = 'build'

                c.execute("INSERT INTO {tn} ({cn}, {cs}, {cb}) VALUES (\"{v1}\", {v2}, {v3})".\
                    format(tn=table_name, cn=column_name, cs=column_sample, cb=column_build, v1=data_point[0], v2=(data_point[1]), v3=build_number))

            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

        try:
            table_name = 'Build_time'
            column_name = 'build_number'
            column_duration = 'build_duration'
            print(build_duration)
            c.execute(("INSERT INTO {tn} ({cn}, {cd}) VALUES ({v1}, {v2})").\
                format(tn=table_name, cn=column_name, cd=column_duration, v1=build_number, v2=build_duration))
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

        conn.commit()
        conn.close()
        return 0
        #try:
        #    os.rename("data.csv", str(job["lastBuild"]["number"]) + ".csv")
    except IOError:
        print("Could not open file")
        return -1
