import os
import requests
import subprocess
import time
import win32api

print("Starting Thomas")
EditorReturn = os.system("editor.exe.lnk")
print("Starting Concussion ball")
time.sleep(10)
gameReturn = os.system("game.exe.lnk")
time.sleep(30)
os.system("taskkill /IM My.exe /t")
print("Starting crunch of data")
results = runTestsAndUploadResultsToDb(gameReturn, EditorReturn)
print("All done, now showing page")

if (gameReturn and EditorReturn):
    return 0
else:
    return -1
