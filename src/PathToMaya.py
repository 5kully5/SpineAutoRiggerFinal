import sys

pjrPath = "D:/profile redirect/culwell/Desktop/New folder/SpineAutoRiggerFinal/src" #have to change this bassed off system
moduleDir = "D:/profile redirect/culwell/Desktop/New folder/" #This aswell but you just have to select the first file

if pjrPath not in sys.path:
    sys.path.append(pjrPath)

if moduleDir not in sys.path:
    sys.path.append(moduleDir)
    