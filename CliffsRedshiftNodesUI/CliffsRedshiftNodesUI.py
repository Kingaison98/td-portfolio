from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.cmds as mc
import maya.OpenMayaUI

'''
import CliffsRedshiftNodesUI as ui
reload(ui)
ui.runNodeUI()
'''

def get_maya_window():

    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class nodeDialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        maya_main = get_maya_window()
        
        super(nodeDialog, self).__init__(maya_main)
        
        self.setWindowTitle("Arnold to Redshift Nodes.")
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets(self):
        self.mainLabel = QtWidgets.QLabel("Enter name of shader:", alignment= QtCore.Qt.AlignCenter)
        self.nodeName = QtWidgets.QLineEdit()
        self.runBtn = QtWidgets.QPushButton("Run")
        
    def create_layouts(self):
        
        mainLayout = QtWidgets.QVBoxLayout(self)
        
        mainLayout.addWidget(self.mainLabel)
        mainLayout.addWidget(self.nodeName)
        mainLayout.addWidget(self.runBtn)
    
    def create_connections(self):
        
        self.runBtn.clicked.connect(self.generate_rs_nodes)

    def generate_rs_nodes(self):
        
        #Declare material Name
        matName = self.nodeName.text()
    
        #Generate redshift material
        redMtName = "{0}_rsMAT".format(matName)
        mc.shadingNode('RedshiftMaterial', asShader = True, name = redMtName)
    
        #Generate noise to ramp layer
        ntrName = "NoiseToRamp_{0}".format(matName)
        mc.shadingNode('RedshiftColorLayer', asUtility = True, name = ntrName)
    
        #Generate diffuse to comp layer
        dtcName = "DiffToComp_{0}".format(matName)
        mc.shadingNode('RedshiftColorLayer', asUtility = True, name = dtcName)
    
def runNodeUI():

    try:
    
        nodeRun.close()

    except:
    
        pass

    nodeRun = nodeDialog()
    nodeRun.show()