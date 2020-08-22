'''
UI module for BatchExportAnimation script
Created by: Aison King
'''

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
from pymel.core import *
import pymel.util
import maya.OpenMayaUI
import BatchExportAnimation

def get_maya_window():

    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)

def runUI():

    try:
    
        exportDialog.close()

    except:
    
        pass

    exportDialog = BatchExportDialog()
    exportDialog.show()


class BatchExportDialog(QtWidgets.QDialog):

    def __init__(self):

        maya_main = get_maya_window()
        reload(BatchExportAnimation)

        super(BatchExportDialog, self).__init__(maya_main)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.setMinimumWidth(400)
        self.setMinimumHeight(100)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        self.titleText = QtWidgets.QLabel("Export Animation")
        self.titleText.setAlignment(QtCore.Qt.AlignHCenter)
        
        #Create a line edit for character rig scene
        self.rigText = QtWidgets.QLabel()
        self.rigText.setText("Rig:")
        self.rigLineEdit = QtWidgets.QLineEdit()
        self.rigBtn = QtWidgets.QPushButton()
        self.rigBtn.setIcon(QtGui.QIcon(":fileOpen.png"))

        #Create a line edit for animation scenes
        self.animText = QtWidgets.QLabel()
        self.animText.setText("Animations:")
        self.animLineEdit = QtWidgets.QLineEdit()
        self.animBtn = QtWidgets.QPushButton()
        self.animBtn.setIcon(QtGui.QIcon(":fileOpen.png"))

        #Create a line edit for the file path to export to
        self.destText = QtWidgets.QLabel()
        self.destText.setText("Destination:")
        self.destLineEdit = QtWidgets.QLineEdit()
        self.destBtn = QtWidgets.QPushButton()
        self.destBtn.setIcon(QtGui.QIcon(":fileOpen.png"))

        self.runBtn = QtWidgets.QPushButton("Export")

    def create_layouts(self):

        mainLayout = QtWidgets.QVBoxLayout(self)
        rigLayout = QtWidgets.QHBoxLayout(self)
        animLayout = QtWidgets.QHBoxLayout(self)
        destLayout = QtWidgets.QHBoxLayout(self)

        rigLayout.addWidget(self.rigText)
        rigLayout.addWidget(self.rigLineEdit)
        rigLayout.addWidget(self.rigBtn)

        animLayout.addWidget(self.animText)
        animLayout.addWidget(self.animLineEdit)
        animLayout.addWidget(self.animBtn)

        destLayout.addWidget(self.destText)
        destLayout.addWidget(self.destLineEdit)
        destLayout.addWidget(self.destBtn)

        mainLayout.addWidget(self.titleText)
        mainLayout.addLayout(rigLayout)
        mainLayout.addLayout(animLayout)
        mainLayout.addLayout(destLayout)
        mainLayout.addWidget(self.runBtn)

    def create_connections(self):

        self.rigBtn.clicked.connect(self.browse_rig_file)
        self.animBtn.clicked.connect(self.browse_anim_files)
        self.destBtn.clicked.connect(self.browse_dest_path)
        self.runBtn.clicked.connect(self.export_anim)

    #Brings up a file dialog to set file line edit
    def browse_rig_file(self):
  
        rigFile = QtWidgets.QFileDialog.getOpenFileName(self, "Get rig File", None, "Maya Scenes (*.mb *.ma)")[0]

        if rigFile:

            self.rigLineEdit.setText(rigFile)
    
    def browse_anim_files(self):
  
        animList = QtWidgets.QFileDialog.getOpenFileNames(self, "Get animation files", None, "Maya Scenes (*.mb *.ma")[0]

        if animList:

            self.animLineEdit.setText(','.join(animList))
    
    def browse_dest_path(self):
        
        destPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Get destination directory", None, 
                                                                QtWidgets.QFileDialog.ShowDirsOnly)

        if destPath:

            self.destLineEdit.setText(destPath)
    
    def export_anim(self):

        rigFile = self.rigLineEdit.text()

        animList = self.animLineEdit.text().split(',')

        destPath = self.destLineEdit.text()

        BatchExportAnimation.batch(rigFile, animList, destPath)

        self.close()
        
    

        