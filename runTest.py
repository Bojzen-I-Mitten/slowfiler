import os
import requests
import subprocess
import time
import win32api

print("Starting Thomas")
print(os.system("editor.exe.lnk"))
print("Starting Concussion ball")
time.sleep(10)
print(os.system("game.exe.lnk"))
print("Starting crunch of data")
results = runTestsAndUploadResultsToDb()
print("All done, now showing page")
