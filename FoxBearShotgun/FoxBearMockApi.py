def getAllTasks():
    return [["This is the first test task","This is the task type","This is the artist space","This is the completion rate","0010"],
            ["Test02","TestType02","TestArtist02","TestComp02","0020"],["Test03","TestType03","TestArtist03","TestComp03","0030"],["4","4A","4B","4C","0040"]]

class MockSG():

    def __init__(self):
        self.tasks = getAllTasks()

    def Task(self, id):
        return

    def getNewestVersion(self):
        return


sg = MockSG()
