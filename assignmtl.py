import glob
import os

##This script re-assign .mtl files to .obj files from Houidni.
##Place this script in the folder where obj and mtl files are. and run script.



objfiles = glob.glob("./*.obj")



for obj in objfiles:
    filename = os.path.basename(obj)
    num = str(filename.split('f')[1].split('.')[0])
    newline = "mtllib MatLib-F%s.mtl" %num + "\n"+"usemtl atlasTextureMap"
    with open(filename, 'r') as f:
        contents = f.read()
        newcontents = contents.replace("usemtl /mat/principledshader", newline)
    
    with open(filename, 'w') as f:
        f.write(newcontents)
    print(newcontents)

