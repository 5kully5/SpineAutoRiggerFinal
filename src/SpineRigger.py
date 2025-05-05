import importlib
import MayaTools
importlib.reload(MayaTools)

from MayaTools import MayaWindow
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QColorDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSlider, QVBoxLayout, QWidget
from PySide2.QtCore import Qt, Signal
from maya.OpenMaya import MVector
import maya.cmds as mc
import maya.mel as mel

class LimbRigger:
    def __init__(self):
        self.root = ""
        self.end = ""
        self.controllerSize = 5
        self.ControllterType = [0]
        self.ControllerColor = [0,0,0]

    def FindVertsBasedOnSelection(self):
        try:
            self.root = mc.ls(sl=True, type="vtx")[0]
            self.end = mc.listRelatives(self.root, c=True, type="vtx")[0]
        except Exception as e:
            raise Exception("Wrong Selection, please select the begining and end of verts")
        
    def CreateBoxController(self, name):
        #copy the mel code you get from maya and import it into here after name
        mel.eval(f"curve -n {name} -d 1 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p 0.5 0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 ;")
        mc.scale(self.controllerSize, self.controllerSize, self.controllerSize, name)
        mc.makeIdentity(name, apply=True) #freeze tranformation
        grpName = name + "_grp"
        mc.group(name, n = grpName)
        return name, grpName
        
class LimbRiggerWidget(MayaWindow):
    def __init__(self):
        super().__init__()
        self.rigger = LimbRigger()
        self.setWindowTitle("Auto Limb Rigger")

        self.mastLayout = QVBoxLayout()
        self.setLayout(self.mastLayout)

        toolTipLable = QLabel("Select the first Vertex, then select the final Vetex, Finally click the auto rig button to rig")
        self.mastLayout.addWidget(toolTipLable)

        autoFindVtxBtn = QPushButton("Auto Find")
        autoFindVtxBtn.clicked.connect(self.FindVtxBtnClicked)
        self.masterLayout.addWidget(autoFindVtxBtn)

        ctrlSizeSlider = QSlider()
        ctrlSizeSlider.setOrientation(Qt.Horizontal)
        ctrlSizeSlider.setRange(1, 30)
        ctrlSizeSlider.setValue(self.rigger.controllerSize)
        self.ctrlSizeLabel = QLabel(f"{self.rigger.controllerSize}")
        ctrlSizeSlider.valueChanged.connect(self.CtrlSizeSliderChanged)

    def CtrlSizeSliderChanged(self, newvalue):
        self.ctrlSizeLabel.setText(f"{newvalue}")
        self.rigger.controllerSize = newvalue

    def FindVtxBtnClicked(self):
        try:
            self.rigger.FindVertsBasedOnSelection()
        except Exception as e:
            QMessageBox.critical(self, "error", f"[{e}]")

LimbRiggerWidget = LimbRiggerWidget()
LimbRiggerWidget.show()