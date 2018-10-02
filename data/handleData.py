import re
import sqlite3
import os
from discord_hooks import Webhook

import jenkins


functionDict = {}

returnCode = os.system("ThomasEditor.exe")

print(returnCode)

try:
    with open("227.csv", "r") as ins:
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

    with open('csvfile.csv', 'wb') as file:
        for functionName in functionDict:
            average_frame_time = (functionName, sum(functionDict[functionName]) / len(functionDict[functionName]),
            max(functionDict[functionName]), min(functionDict[functionName]))
            graph_data.append(average_frame_time)


    print(graph_data)


    url = 'https://discordapp.com/api/webhooks/489031312032923649/m_DPPOX33J1unuGYKHnHYtEID2qkYmKYNj5yEjajmfc0yxnT0iwm69k18fz6rE8DsRcD'

    #msg = Webhook(url,msg="sluta vara en gaylord mogge" % (graph_data))
    #msg.post()


    sqlite_file = 'C:\\test.db'
    table_name = 'Build'
    column_name = 'name'
    column_sample = 'samples'
    column_build = 'build'

    j = jenkins.Jenkins("http://192.168.1.141:8080", "admin", "jenkinsjenkar")
    job =  j.get_job_info("SSP")

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    for data_point in graph_data:
        try:
            c.execute("INSERT INTO {tn} ({cn}, {cs}, {cb}) VALUES (\"{v1}\", {v2}, {v3})".\
                format(tn=table_name, cn=column_name, cs=column_sample, cb=column_build, v1=data_point[0], v2=(data_point[1]), v3=job["lastBuild"]["number"]))
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))


    conn.commit()
    conn.close()
    os.rename("data.csv", str(job["lastBuild"]["number"]) + ".csv")
except IOError:
    print("Could not open file")
