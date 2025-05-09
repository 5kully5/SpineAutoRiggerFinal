# My Maya Plugin

## Spine Rigger

[Spine Rigger]("./src/SpineRigger.py")

to start make sure the correct path to your pc is implimented in [PathToMaya]("./src/PathToMaya.py")

Grab your mesh and go into verticies

select two points a starting and end point then click add bone

when thats done select the whole bone then click rig

this will add a constraint parent it to the middle bone then thats it

<<<<< How the Bone works

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
==========
            

<<<<<< This is how the you can switch the main bone