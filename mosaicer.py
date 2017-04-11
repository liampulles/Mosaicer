#!/usr/bin/env python

from PIL import Image
import sys, getopt
from io import StringIO, BytesIO

def printusage():
    print("""mosaicer.py -i <inputfile> -o <outputfile>
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
            #Red part
            pixelsout[x,y] = (pixelsin[x,y][0],0,0)
        elif (x%2==0)&(y%2==1):
            #Blue part
            pixelsout[x,y] = (0,0,pixelsin[x,y][2])
        else:
            #Green part
            pixelsout[x,y] = (0,pixelsin[x,y][1],0)

if outputfile == '-':
    out = BytesIO()
    outputimage.save(out,inputimage.format)
    sys.stdout.buffer.write(out.getvalue())
else:
    outputimage.save(outputfile)
