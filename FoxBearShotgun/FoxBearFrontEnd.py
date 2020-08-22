from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import FoxBearMockApi as api

class TaskListModel(QAbstractTableModel):
    def __init__(self, ui, parent, tasks, *args):
        super().__init__(parent, *args)
        self.taskList = tasks.copy()
        self.dataTable = tasks.copy()
        self.ui = ui
        self.parentTable = parent
        self.header = ["Name", "Type", "Artist", "Status", "ID"]
        self.selected = None

    def setNewTaskList(self, tasks):
        self.taskList = tasks
        self.updateData(self.taskList, self.ui.filterList)

    #Sets public selected variable
    def selectID(self):
        id = self.ui.taskTable.selectedIndexes()[4]
        selectedID = self.ui.taskTable.model().data(id, Qt.DisplayRole)
        print(selectedID)
        self.selected = selectedID

    def updateData(self, taskList, filters):
        self.layoutAboutToBeChanged.emit()
        self.dataTable = self.taskList.copy()
        filteredItems = []
        if not filters == {"artist": [], "status": [], "type": []}:
            for x in self.dataTable:
                valid = True
                for filterCategory in filters:
                    categorySatisfied = False
                    if filters.get(filterCategory) != []:
                        for y in filters.get(filterCategory):
                          if y in x:
                             categorySatisfied = True
                             break
                        if categorySatisfied == False:
                           valid = False
                if valid == False:
                    filteredItems.append(x)
        for x in filteredItems:
            print("Removing", x)
            xIndex = self.dataTable.index(x)
            self.removeRow(xIndex, QModelIndex())
            self.dataTable.remove(x)
        #print(self.dataTable)
        self.layoutChanged.emit()

    def rowCount(self, QModelIndex = None):
        return len(self.dataTable)

    def columnCount(self, QModelIndex = None):
        if len(self.dataTable) > 0:
            return len(self.dataTable[0])
        else:
            return 0

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            value = self.dataTable[index.row()][index.column()]
            return value
        else:
            return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

class filterItem(QAction):
    def __init__(self, ui, string, filterType, parent):
        super().__init__(string, parent, checkable = True)
        self.type = filterType
        self.ui = ui
        self.triggered.connect(self.updateFilters)

    def updateFilters(self):
        filterList = self.ui.filterList
        if self.type == "Artist":
            if self.isChecked() == True:
                filterList["artist"].append(self.text())
            else:
                filterList["artist"].remove(self.text())
        if self.type == "Status":
            if self.isChecked() == True:
                filterList["status"].append(self.text())
            else:
                filterList["status"].remove(self.text())
        if self.type == "Type":
            if self.isChecked() == True:
                filterList["type"].append(self.text())
            else:
                filterList["type"].remove(self.text())
        self.ui.taskModel.updateData(self.ui.taskList, self.ui.filterList)

class FoxBearUI(QWidget):

    def __init__(self):
        super(FoxBearUI, self).__init__()

        self.taskList = []
        self.filterList = {"artist": [], "status": [], "type": []}
        self.selectedID = None
        self.taskTable = QTableView(self, cornerButtonEnabled=False)
        self.taskModel = TaskListModel(self, self.taskTable, self.taskList)

        self.initLayout()
        self.initButtons()

        self.initMenus()
        self.refreshTasks()
        self.loadTaskTable(self.taskList)


    def initLayout(self):
        self.setWindowTitle("Vernal Production Sheet")
        self.layout = QGridLayout()
        self.layout.setVerticalSpacing(10)
        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnMinimumWidth(0, 400)
        self.setLayout(self.layout)
        self.layout.addWidget(self.taskTable, 0, 0, Qt.AlignCenter)

    def initButtons(self):
        buttonArea = QGroupBox()
        buttonLayout = QHBoxLayout()
        self.refreshBtn = QPushButton("Refresh Tasks")
        self.refreshBtn.pressed.connect(self.refreshTasks)
        self.downloadBtn = QPushButton("Download Video")
        self.downloadBtn.pressed.connect(self.downloadFile)
        buttonLayout.addWidget(self.refreshBtn)
        buttonLayout.addWidget(self.downloadBtn)
        buttonArea.setLayout(buttonLayout)
        self.layout.addWidget(buttonArea, 1, 0, Qt.AlignCenter)

    def initMenus(self):
        self.mainMenu = QMenuBar()
        self.layout.setMenuBar(self.mainMenu)
        self.loadArtistMenu(self.filterList.get("artist"))
        self.loadStatusMenu(self.filterList.get("status"))
        self.loadTypeMenu(self.filterList.get("type"))

    def refreshTasks(self):
        self.taskList = api.getAllTasks()
        for x in self.mainMenu.actions():
            self.mainMenu.removeAction(x)
        self.loadTasks()


    def loadTasks(self):
        self.filterList = {"artist": [], "status": [], "type": []}
        for task in self.taskList:
            if not task[1] in self.filterList["type"]:
                self.filterList["type"].append(task[1])
            if not task[2] in self.filterList["artist"]:
                self.filterList["artist"].append(task[2])
            if not task[3] in self.filterList["status"]:
                self.filterList["status"].append(task[3])
        self.initMenus()

    def loadArtistMenu(self, artistList):
        artistMenu = self.mainMenu.addMenu("&Artists")
        for x in artistList:
            newArtist = filterItem(self, x, "Artist", artistMenu)
            artistMenu.addAction(newArtist)
        artistMenu.show()

    def loadTypeMenu(self, typeList):
        typeMenu = self.mainMenu.addMenu("&Task Type")
        for x in typeList:
            newType = filterItem(self, x, "Type", typeMenu)
            typeMenu.addAction(newType)
        typeMenu.show()

    def loadStatusMenu(self, statusList):
        statusMenu = self.mainMenu.addMenu("&Status")
        for x in statusList:
            newStatus = filterItem(self, x, "Status", statusMenu)
            statusMenu.addAction(newStatus)
        statusMenu.show()

    def loadTaskTable(self, tasks):
        self.taskModel.setNewTaskList(tasks)
        sortProxy = QSortFilterProxyModel()
        sortProxy.setSourceModel(self.taskModel)
        self.taskTable.setModel(sortProxy)
        self.taskTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.taskTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.taskTable.setCornerButtonEnabled(False)
        self.taskTable.setShowGrid(False)
        self.taskTable.setSortingEnabled(True)
        self.taskTable.clicked.connect(self.taskModel.selectID)
        self.taskTable.setMinimumSize(550, 400)
        self.taskTable.setColumnWidth(0, 110)
        self.taskTable.setColumnWidth(1, 110)
        self.taskTable.setColumnWidth(2, 110)
        self.taskTable.setColumnWidth(3, 110)
        self.taskTable.setColumnWidth(4, 110)

    def downloadFile(self):
        if not self.taskModel.selected:
            self.showMessageBox("No ID Selected!")
            return
        selectedID = self.taskModel.selected
        selectedTask = api.sg.Task(id=selectedID)
        try:
            newestVersion = api.getNewestVersion(selectedTask)
        except:
            self.showMessageBox("This task has no versions (make sure there are uploaded movies).")
            return
        if newestVersion['sg_uploaded_movie']:
            SaveWindow = QFileDialog(w, "Where do you want to save this video?")
            SaveWindow.setAcceptMode(QFileDialog.AcceptSave)
            SaveWindow.setFileMode(QFileDialog.Directory)
            SaveWindow.exec()
            filePath = SaveWindow.selectedFiles()[0] + ".mov"
            api.download(newestVersion, filePath)
        else:
            self.showMessageBox("The latest version has no movie!")
            return

    def showMessageBox(self, text):
        MessageWindow = QMessageBox(w, text=text)
        MessageWindow.show()



if __name__ == '__main__':
    app = QApplication([])
    try:
        w.show()
    except:
        w = FoxBearUI()
        w.show()
    app.exec_()

def runUI():
    w = FoxBearUI()
    try:
        w.close()
    except:
        pass
    w.show()


