import hashlib

import sg_wrapper

'''
Shotgun API Library for Finn & Beau Thesis project

These functions were designed for use both within Maya as a utility library, as well as the api driving the FoxBearFrontnd

'''


h = hashlib.sha256()
sg = sg_wrapper.Shotgun("https://lmu.shotgunstudio.com","FoxAPI","yyvtCefciiqtbrddi#cv1tsrc")
fox = sg.Project(name = "Fox")
shots = sg.Shots(project = fox)
tasks = sg.Tasks(project = fox)
shotDir = "//medusa/Fox/Shots"

'''
Returns: A list of all the tasks in the project formatted for FoxBearFrontEnd.
The format returned is as follows
['Entity Code', 'Content', 'Assignees', 'Status', 'ID']
'''
def getAllTasks():
    tasks = sg.Tasks(project = fox)
    frontEndForm = []
    for task in tasks:
        newForm = []
        newForm.append(task['entity']['code'])
        newForm.append(task['content'])
        if task['task_assignees']:
            newForm.append(task['task_assignees'][0]['name'])
        else:
            newForm.append("N/A")
        newForm.append(parseStatus(task['sg_status_list']))
        newForm.append(task['id'])
        frontEndForm.append(newForm)
    return frontEndForm

'''
Given a task, will return a Version object that is the newest Version attached to that task
'''
def getNewestVersion(task):
    taskType = task['content']
    shot = task['entity']
    versions = sg.Versions(sg_task = task)
    if versions == []:
        return Exception("No versions found.")
    newestVersion = versions[0]
    for ver in versions:
        if ver['created_at'] > newestVersion['created_at']:
            newestVersion = ver
    return newestVersion

'''
Calls SG download_attachment function given a Version and path, use getNewestVersion() for first argument
'''
def download(version, path):
    movie = version['sg_uploaded_movie']
    sg._sg.download_attachment(movie['id'], path)

'''
A switch table function to parse strings from shotgun data format to FoxBearFrontEnd format
Returns opposite status string from one passed in
'''
def parseStatus(str):
    switchTable = {
        "wtg": "Waiting",
        "fin": "Final",
        "ip": "In Progress",
        "hld": "On Hold",
        "rdy": "Ready to Start",
        "rev": "Review",
        "Waiting": "wtg",
        "Final": "fin",
        "In Progress": "ip",
        "On Hold": "hld",
        "Ready to Start": "rdy",
        "Review": "rev"
    }
    return switchTable.get(str)