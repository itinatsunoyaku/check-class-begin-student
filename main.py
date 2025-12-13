import requests

info = {
    "name": "Name",
    "no": "StudentID",
    "class": "Class"}

def IsAlive():
    respond=requests.get("Ip/IsAlive")
    if respond == "True":
        return True
    elif respond == "overtime" :
        return False
    else:
        print("未找到服务器")
        return False

def MyId():
    respond=requests.get("Ip/MyId")
    return respond

def CheckIn():
    respond = requests.post("/CheckIn",info)
    return 0

if IsAlive():
    MyId()
if IsAlive():
    CheckIn()
