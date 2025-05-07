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
        self.mid = ""
        self.end = ""
        self.FirstBone = ""
        self.EndBone = ""
        self.controllerSize = 5
        self.ControllterType = [0]
        self.BoneAmmount = 12
        self.joints = []

    def FindsJntsOnSelected(self):
        self.root = mc.ls(sl= True, type="joint")
        self.mid = mc.listRelatives(self.root, c=True, type="joint")[0]
        self.end = mc.listRelatives(self.mid, c=True, type="joint")[0]
    
    def CreateBoxController(self, name):
        #copy the mel code you get from maya and import it into here after name
        mel.eval(f"curve -n {name} -d 1 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p 0.5 0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 ;")
        mc.scale(self.controllerSize, self.controllerSize, self.controllerSize, name)
        mc.makeIdentity(name, apply=True) #freeze tranformation
        grpName = name + "_grp"
        mc.group(name, n = grpName)
        return name, grpName
        
        jntsListLineEdit

    def FindVertsBasedOnSelection(self):
        selectedPnts = mc.ls(sl=True)
        self.FirstBone = selectedPnts[0]
        self.EndBone = selectedPnts[1]

        # get root position
        rootPos = self.GetPointPositionAsMVetor(self.FirstBone)

        # get end poition
        endPos = self.GetPointPositionAsMVetor(self.EndBone)

        spineVector: MVector =  endPos - rootPos
        
        spineLength = spineVector.length()
        
        spineVector.normalize()

        segmentLenght = spineLength / (self.BoneAmmount - 1)

        mc.select(cl=True)
        
        self.joints = []
        for i in range(0, self.BoneAmmount):
            scalar = i * segmentLenght
            bonePos = rootPos + spineVector * scalar
            print(bonePos.z)
            newJnt = mc.joint(p=(bonePos.x, bonePos.y, bonePos.z))
            self.joints.append(newJnt)

        print(selectedPnts)

    def ChangeJntOrder(self):
        mc.reroot(self.joints[-1])


    def GetPointPositionAsMVetor(self, point):
        # get point position
        x, y, z = mc.pointPosition(point)
        return MVector(x, y, z)

    def CreateBoxController(self, name):
        #copy the mel code you get from maya and import it into here after name
        mel.eval(f"curve -n {name} -d 1 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p 0.5 0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 ;")
        mc.scale(self.controllerSize, self.controllerSize, self.controllerSize, name)
        mc.makeIdentity(name, apply=True) #freeze tranformation
        grpName = name + "_grp"
        mc.group(name, n = grpName)
        return name, grpName
    
    def RigLimb(self):
        rootCtrl, rootCtrlGrp = self.CreateFKControllerForJnts(self.root)
        midCtrl, midCtrlGrp = self.CreateFKControllerForJnts(self.root)
        endCtrl, endCtrlGrp = self.CreateFKControllerForJnts(self.root)

        mc.parent(midCtrlGrp, rootCtrl)
        mc.parent(endCtrlGrp, midCtrl)
        #making the bones link to the controller

        ikEndCtrl = "ac_ik_" + self.end
        ikEndCtrl, ikEndCtrlGrp = self.CreateBoxController(ikEndCtrl)
        mc.matchTransformation(ikEndCtrlGrp, self.end)
        endOrientConstraint = mc.orientConstraint(ikEndCtrl, self.end)[0]

        rootJntLoc = self.GetObjectLocation(self.root)
        self.PrintMVector(rootJntLoc)

        ikHandleName = "ikHandle_" + self.end
        mc.ikHandle(n=ikHandleName, sol="IkRPsolver", sj=self.root, ee=self.end)

        poleVectorLocationValues = mc.getAttr(ikHandleName + ".poleVector")[0]
        poleVector = MVector(poleVectorLocationValues[0], poleVectorLocationValues[1], poleVectorLocationValues[2])
        poleVector.normal()

        endJntLoc = self.GetObjectLocation(self.end)
        rootToEndVector = endJntLoc - rootJntLoc

        poleVectorCtrlLoc = rootJntLoc + rootToEndVector / 2 + poleVector * rootToEndVector.length()
        poleVectorCtrl = "ac_ik" + self.mid
        mc.spaceLocator(n=poleVectorCtrl)
        poleVectorCtrlGrp = poleVectorCtrl + "_grp"
        mc.group(poleVectorCtrl, n= poleVectorCtrlGrp)
        mc.setAttr(poleVectorCtrlGrp+"t", poleVectorCtrlLoc.x, poleVectorCtrlLoc.y, poleVectorCtrlLoc.z, typ="double3")

        mc.poleVectorConstraint(poleVectorCtrl, ikHandleName)

        ikfkBlendCtrl = "ac_ikfk_blend_" + self.root
        ikfkBlendCtrl, ikfkBlendCtrlGrp = self.CreatePlusController(ikfkBlendCtrl)
        mc.seltAttr(ikfkBlendCtrlGrp+ ".t", rootJntLoc.x*2, rootJntLoc.y, rootJntLoc.z*2, typ="double3")

        ikfkBlendAttrName = "ikfkBlend"
        mc.addAttr(ikfkBlendCtrl, ln=ikfkBlendAttrName, min = 0, max = 1, k=True)
        ikfkBlendAttr = ikfkBlendCtrl + "." + ikfkBlendAttrName

        mc.expression(s=f"{ikHandleName}.ikBlend={ikfkBlendAttr}")
        mc.expression(s=f"{ikEndCtrlGrp}.v={poleVectorCtrlGrp}.v={ikfkBlendAttr}")
        mc.expression(s=f"{rootCtrlGrp}.v=1-{ikfkBlendAttr}")
        mc.expression(s=f"{endOrientConstraint}.{endCtrl}w0 = 1-{ikfkBlendAttr}")
        mc.expression(s=f"{endOrientConstraint}.{ikEndCtrl}w0 = {ikfkBlendAttr}")

        topGrpName = f"{self.root}_rig_grp"
        mc.group([rootCtrlGrp, ikEndCtrlGrp, poleVectorCtrlGrp, ikfkBlendCtrlGrp], n=topGrpName)
        mc.parent(ikHandleName, ikEndCtrl)

        mc.setAttr(topGrpName+".overrideEnable", 1)
        mc.setAttr(topGrpName+".overrideRGBColors", 1)
        mc.setAttr(topGrpName+".overrideRGBColors", self.ControllerColor[0], self.ControllerColor[1], self.ControllerColor[2], type="double3")
        
class LimbRiggerWidget(MayaWindow):
    def __init__(self):
        super().__init__()
        self.rigger = LimbRigger()
        self.setWindowTitle("Auto Limb Rigger")

        self.masterlayout = QVBoxLayout()
        self.setLayout(self.masterlayout)

        toolTipLable = QLabel("Select the first Vertex, then select the final Vetex, Finally click the auto rig button to rig")
        self.masterlayout.addWidget(toolTipLable)

        autoFindVtxBtn = QPushButton("Auto Bone")
        autoFindVtxBtn.clicked.connect(self.FindVtxBtnClicked)
        self.masterlayout.addWidget(autoFindVtxBtn)

        ctrlSizeSlider = QSlider()
        ctrlSizeSlider.setOrientation(Qt.Horizontal)
        ctrlSizeSlider.setRange(1, 30)
        ctrlSizeSlider.setValue(self.rigger.controllerSize)
        self.ctrlSizeLabel = QLabel(f"{self.rigger.controllerSize}")
        ctrlSizeSlider.valueChanged.connect(self.CtrlSizeSliderChanged)
        self.masterlayout.addWidget(ctrlSizeSlider)

        BoneSlider = QSlider()
        BoneSlider.setOrientation(Qt.Horizontal)
        BoneSlider.setRange(1, 100)
        BoneSlider.setValue(self.rigger.BoneAmmount)
        self.BonesLabel = QLabel(f"{self.rigger.BoneAmmount}")
        BoneSlider.valueChanged.connect(self.ChangeAmmountOfBones)
        self.masterlayout.addWidget(BoneSlider)

        rigLimbBtn = QPushButton("Rig Limb")
        rigLimbBtn.clicked.connect(lambda : self.rigger.RigLimb())
        self.masterlayout.addWidget(rigLimbBtn)

        ctrlrButton = QPushButton("ChangeBoneDirection")
        ctrlrButton.clicked.connect(self.ChangeBoneDirection)
        self.masterlayout.addWidget(ctrlrButton)
         #jointChain
    
    def ChangeAmmountOfBones(self, newvalue):
        self.BonesLabel.setText(f"{newvalue}")
        self.BonesLabel.BoneAmmount = newvalue

    def CtrlSizeSliderChanged(self, newvalue):
        self.ctrlSizeLabel.setText(f"{newvalue}")
        self.rigger.controllerSize = newvalue

    def ChangeBoneDirection(self):
        self.rigger.ChangeJntOrder()
        
    def FindVtxBtnClicked(self):
        try:
            self.rigger.FindVertsBasedOnSelection()
        except Exception as e:
            QMessageBox.critical(self, "error", f"[{e}]")

    

LimbRiggerWidget = LimbRiggerWidget()
LimbRiggerWidget.show()