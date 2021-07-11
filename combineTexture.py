from PIL import Image
import os
import sys
args = sys.argv
def combineTexture(imglist):
    print(imglist)
    imglist = imglist.split(',')
    sep = os.path.sep
    splitpoint = str(imglist[0]).rfind(sep)
    currentpath = str(imglist[0])[0:splitpoint+1]
    newfolder = os.path.join(currentpath, "combined")
    os.mkdir(newfolder) 
    imgnum = 0
    texnum = 0
    newfilelist = []
    base = None
    for idx, im in enumerate(imglist):
        imgnum = idx % 4
        texnum = idx // 4 + 1
        f = Image.open(im)
        if(imgnum == 0):
            imagesize = f.size[0] * 2
            new = Image.new(mode='RGB', size = (imagesize, imagesize), color =(255, 255, 255))
            base = new.copy()
            base.paste(f, (0, 0))
        elif(imgnum == 1):
            base.paste(f, (f.size[0], 0))
        elif(imgnum == 2):
            base.paste(f, (f.size[0], f.size[0]))
        elif(imgnum == 3):
            base.paste(f, (0, f.size[0]))
        if(imgnum == 3 or idx == len(imglist) - 1):
            base.resize(f.size)
            newfilepath = newfolder + "//newatlas-%s.jpg" %str(texnum)
            base.save(newfilepath, quality=95)
            newfilelist.append(newfilepath)
    with open(newfolder + "//texturelist.txt", 'w') as f:
        f.write("\n".join(newfilelist))
        f.truncate()
##args = "J:/TerrySwing/sparkAR/testTextures/atlas-f00001.png,J:/TerrySwing/sparkAR/testTextures/atlas-f00002.png,J:/TerrySwing/sparkAR/testTextures/atlas-f00003.png,J:/TerrySwing/sparkAR/testTextures/atlas-f00004.png,J:/TerrySwing/sparkAR/testTextures/atlas-f00005.png,J:/TerrySwing/sparkAR/testTextures/atlas-f00006.png,J:/TerrySwing/sparkAR/testTextures/atlas-f00007.png,J:/TerrySwing/sparkAR/testTextures/atlas-f00008.png,J:/TerrySwing/sparkAR/testTextures/atlas-f00009.png"

if len(sys.argv) < 1:
    print('Not enough argument is provided')
    sys.exit(1)
combineTexture(args[1])