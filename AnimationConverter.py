import pymel.core as pm
import os
import subprocess
from subprocess import PIPE
def getframenum(obj):
    num = str(obj).split(":")[0].split("f")[1]
    meshnum = float(format(int(num), '1d'))
    return meshnum
##def bindJoints(obj):
    ##pm.select(clear = True)
    ##meshname = str(obj)
    ##jointname = meshname + "_jnt"
    ##pm.joint( n=jointname, p=(0, 0, 0) )
    ##pm.skinCluster(jointname, meshname, dr=4.5)
    ##return jointname
def uvtransform(objs):
    num = 0
    matnum = 0
    matgroup = {}
    for obj in objs:
        if(num == 0):
            matnum += 1
            matgroup[matnum] = [obj]
            pm.select(obj.map)
            pm.polyEditUV(pivotU=0, pivotV=1, scaleU=0.5, scaleV=0.5)
            pm.select(cl=True)
            num += 1
        elif(num == 1):
            matgroup[matnum].append(obj)
            pm.select(obj.map)
            pm.polyEditUV(pivotU=1, pivotV=1, scaleU=0.5, scaleV=0.5)
            pm.select(cl=True)
            num += 1
        elif(num == 2):
            matgroup[matnum].append(obj)
            pm.select(obj.map)
            pm.polyEditUV(pivotU=1, pivotV=0, scaleU=0.5, scaleV=0.5)
            pm.select(cl=True)
            num += 1
        elif(num == 3):
            matgroup[matnum].append(obj)
            pm.select(obj.map)
            pm.polyEditUV(pivotU=0, pivotV=0, scaleU=0.5, scaleV=0.5)
            pm.select(cl=True)
            num = 0
    return matgroup
def assignMaterial(matgroup, newfilenames):
    for i in range(len(matgroup)):
        matname = "combinedtexture_" + str(i+1)
        shader = pm.shadingNode('lambert', asShader=1, name=matname)
        filenode=pm.shadingNode('file',asTexture=True, n = "tex")
        SG = pm.sets(renderable=True,noSurfaceShader=True,empty=True)
        pm.setAttr( '%s.fileTextureName' % filenode, newfilenames[i], type = "string")
        pm.connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %SG)
        pm.connectAttr('%s.outColor' %filenode,'%s.color' %shader)
        for mesh in matgroup[i+1]:
            pm.sets(SG, e=1, forceElement=mesh)
def getTexturefile(obj, sep):
    sg = pm.listConnections(obj.getShape(), type='shadingEngine')
    sginfo = pm.listConnections(sg[0], type='materialInfo')
    filenode = pm.listConnections(sginfo[0], type='file')
    filename = str(pm.getAttr(filenode[0].fileTextureName))
    if(sep == '\\'):
        (filename.replace('/', '\\'))
    filename = os.path.normpath(filename)
    return filename
def combinetexture(texturelist, sep, pPath, scriptPath):
    if(sep == '/'):
        ## For OSX environment
        ##command ='usr/bin/python' + ' ' + 'Users/Desktop/3k/combineTexture.py' + " " + texturelist
        command = pPath + ' ' + scriptPath + " " + texturelist
    else:
        ## For windows environment 
        ##command = [r'C:\\Users\\usr\\AppData\\Local\\Microsoft\\WindowsApps\\Python.exe', '-i', r'J:\\combineTexture.py']
        command = [pPath,'-i', scriptPath]
        command.append(texturelist)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = proc.communicate()
    if proc.returncode != 0:
        print("subprocess is failed")
    basepath = os.path.split(texturelist.split(',')[0])[0]
    if(sep == '\\'):
        path = "combined\\texturelist.txt"
    elif(sep == '/'):
        path = "combined/texturelist.txt"
    newpath = os.path.join(basepath, path)
    with open(newpath, 'r') as f:
        filelist = [s.strip() for s in f.readlines()]
    return filelist
def main(paths):
    startframe = pm.playbackOptions(ast=True, q=True)
    endframe = pm.playbackOptions(aet=True, q=True)
    objs = pm.selected()
    pm.group( em=True, n='notinuse' )
    meshlist = []
    texturefiles = ''
    sep = os.path.sep
    for idx, obj in enumerate(objs):
        frame = getframenum(obj)
        if(frame%2 != 0):
            target = obj
            ##target = bindJoints(obj)
            if(frame == startframe):
                pm.setKeyframe(obj, v=1, itt='linear', at='scale', t=frame)
                pm.setKeyframe(obj, v=1, itt='linear', at='scale', t=frame+1.9999)
                pm.setKeyframe(obj, v=0.001, itt='linear', at='scale', t=frame+2)
            elif(frame == endframe):
                pm.setKeyframe(obj, v=0.001, itt='linear', at='scale', t=frame-1)
                pm.setKeyframe(obj, v=1, itt='linear', at='scale', t=frame-1.9999)
                pm.setKeyframe(obj, v=1, itt='linear', at='scale', t=frame)
            else:
                pm.setKeyframe(obj, v=0.001, itt='linear', at='scale', t=frame-0.0001)
                pm.setKeyframe(obj, v=1, itt='linear', at='scale', t=frame)
                pm.setKeyframe(obj, v=1, itt='linear', at='scale', t=frame+1.9999)
                pm.setKeyframe(obj, v=0.001, itt='linear', at='scale', t=frame+2)
            texturefiles += getTexturefile(obj, sep)
            if(len(objs)-3 >= idx):
                texturefiles += ','
            meshlist.append(obj)
        else:
            pm.parent(obj, "notinuse")
        pm.setAttr('notinuse.visibility', 0)
    matgroup = uvtransform(meshlist)
    newtextures = combinetexture(texturefiles, sep, paths[0], paths[1])
    assignMaterial(matgroup, newtextures)
win = pm.window(title="Mesh Sqequence Converter",sizeable = False)
layout = pm.rowColumnLayout(numberOfColumns = 1, columnAttach = (1, 'both', 0), columnWidth = (500,300))
pm.text(label = "Path for Python")
pathforPython = pm.textField(tx = "usr/bin/python", width = 500)
pm.text(label = "Path for conbineTexture.py")
pathforScript = pm.textField(tx = "Users/tomo/Desktop/3k/combineTexture.py", width = 500)
pm.button(label = "Convert Mesh Animation", command = "main((pm.textField(pathforPython, q=True, tx=True), pm.textField(pathforScript, q=True, tx=True)))")
pm.button(label = "Close window", command = "pm.deleteUI(win, window=True)",w = 500)
win.show()