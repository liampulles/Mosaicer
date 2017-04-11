#!/usr/bin/env python

from PIL import Image
import sys, getopt
from io import StringIO, BytesIO

def printusage():
    print("""bilinear.py -i <inputfile> -o <outputfile>
    STDIN and STDOUT input/output can be specified by "-" where appropriate (minus quotes). STDOUT output will be in PNG format.
    """, file=sys.stderr)

inputfile = ''
outputfile = ''
try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:o:")
except getopt.GetoptError:
    printusage()
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        printusage()
        sys.exit()
    elif opt == '-i':
        inputfile = arg
    elif opt == '-o':
        outputfile = arg
if inputfile == '':
    printusage()
    sys.exit(2)
if outputfile == '':
    printusage()
    sys.exit(2)

if inputfile == '-':
    inputimage = Image.open(sys.stdin.buffer)
else:
    inputimage = Image.open(inputfile)

outputimage = Image.new(inputimage.mode,inputimage.size,0)
pixelsin = inputimage.load()
pixelsout = outputimage.load()
for x in range(inputimage.width):
    for y in range(inputimage.height):
        if (x%2==1)&(y%2==0):
            #At red pixel, need green + blue
            gtot=0
            gcount=0
            if (y-1 > 0):
                gcount += 1
                gtot += pixelsin[x,y-1][1]
            if (y+1 < inputimage.height):
                gcount += 1
                gtot += pixelsin[x,y+1][1]
            if (x-1 > 0):
                gcount += 1
                gtot += pixelsin[x-1,y][1]
            if (x+1 < inputimage.width):
                gcount += 1
                gtot += pixelsin[x+1,y][1]
            btot=0
            bcount=0
            if (y-1 > 0)&(x-1 > 0):
                bcount += 1
                btot += pixelsin[x-1,y-1][2]
            if (y-1 > 0)&(x+1 < inputimage.width):
                bcount += 1
                btot += pixelsin[x+1,y-1][2]
            if (y+1 < inputimage.height)&(x+1 < inputimage.width):
                bcount += 1
                btot += pixelsin[x+1,y+1][2]
            if (y+1 < inputimage.height)&(x-1 > 0):
                bcount += 1
                btot += pixelsin[x-1,y+1][2]
            pixelsout[x,y] = (pixelsin[x,y][0],int(gtot/gcount),int(btot/bcount))
        elif (x%2==0)&(y%2==1):
            # At blue pixel, need green + red
            gtot=0
            gcount=0
            if (y-1 > 0):
                gcount += 1
                gtot += pixelsin[x,y-1][1]
            if (y+1 < inputimage.height):
                gcount += 1
                gtot += pixelsin[x,y+1][1]
            if (x-1 > 0):
                gcount += 1
                gtot += pixelsin[x-1,y][1]
            if (x+1 < inputimage.width):
                gcount += 1
                gtot += pixelsin[x+1,y][1]
            rtot=0
            rcount=0
            if (y-1 > 0)&(x-1 > 0):
                rcount += 1
                rtot += pixelsin[x-1,y-1][0]
            if (y-1 > 0)&(x+1 < inputimage.width):
                rcount += 1
                rtot += pixelsin[x+1,y-1][0]
            if (y+1 < inputimage.height)&(x+1 < inputimage.width):
                rcount += 1
                rtot += pixelsin[x+1,y+1][0]
            if (y+1 < inputimage.height)&(x-1 > 0):
                rcount += 1
                rtot += pixelsin[x-1,y+1][0]
            pixelsout[x,y] = (int(rtot/rcount),int(gtot/gcount),pixelsin[x,y][2])
        elif (x%2==0)&(y%2==0):
            #At green pixel, top-left
            btot=0
            bcount=0
            if (y-1 > 0):
                bcount += 1
                btot += pixelsin[x,y-1][2]
            if (y+1 < inputimage.height):
                bcount += 1
                btot += pixelsin[x,y+1][2]
            rtot=0
            rcount=0
            if (x-1 > 0):
                rcount += 1
                rtot += pixelsin[x-1,y][0]
            if (x+1 < inputimage.width):
                rcount += 1
                rtot += pixelsin[x+1,y][0]
            pixelsout[x,y] = (int(rtot/rcount),pixelsin[x,y][1],int(btot/bcount))
        else:
            #At green pixel, bottom-right
            rtot=0
            rcount=0
            if (y-1 > 0):
                rcount += 1
                rtot += pixelsin[x,y-1][0]
            if (y+1 < inputimage.height):
                rcount += 1
                rtot += pixelsin[x,y+1][0]
            btot=0
            bcount=0
            if (x-1 > 0):
                bcount += 1
                btot += pixelsin[x-1,y][2]
            if (x+1 < inputimage.width):
                bcount += 1
                btot += pixelsin[x+1,y][2]
            pixelsout[x,y] = (int(rtot/rcount),pixelsin[x,y][1],int(btot/bcount))


if outputfile == '-':
    out = BytesIO()
    outputimage.save(out,inputimage.format)
    sys.stdout.buffer.write(out.getvalue())
else:
    outputimage.save(outputfile)
