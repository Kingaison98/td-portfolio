from random import *

def getAllTasks():
    taskList = []
    for i in range (1, 9):
        taskName = "Task{0}".format(i)
        taskType = ["Layout","Animation","FX","Comp"][randrange(3)]
        status = ["Waiting","Ready","Incomplete","Complete"][randrange(4)]
        artist = ["James","Sarah","Alex"][randrange(2)]
        taskID = "00{0}0".format(i)
        task = [taskName, taskType, artist, status, taskID]
        taskList.append(task)
    return taskList

class MockSG():

    def __init__(self):
        self.tasks = getAllTasks()

    def Task(self, id):
        return

    def getNewestVersion(self):
        return


sg = MockSG()
