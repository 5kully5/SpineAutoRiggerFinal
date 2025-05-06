import sys

pjrPath = "D:/profile redirect/culwell/Desktop/New folder/SpineAutoRiggerFinal/src"
moduleDir = "D:/profile redirect/culwell/Desktop/New folder/"

if pjrPath not in sys.path:
    sys.path.append(pjrPath)

if moduleDir not in sys.path:
    sys.path.append(moduleDir)
    