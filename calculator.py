from vpython import *
from sympy import N
from symengine import sympify, symbols
from symengine.lib.symengine_wrapper import solve
from math import *
import random

scene.width=900
scene.height=900
scene.autoscale = False
lowerBound = -10
upperBound = 10
loading = False

# X Y Z Assignment
x = (arrow(pos=vector(0,0,0), axis=vector(upperBound+5,0,0), color=color.red, round=True, shaftwidth=.1), arrow(pos=vector(0,0,0), axis=vector(lowerBound-5,0,0), color=color.red, round=True, shaftwidth=.1))
z = (arrow(pos=vector(0,0,0), axis=vector(0,upperBound+5,0), color=color.blue, round=True, shaftwidth=.1), arrow(pos=vector(0,0,0), axis=vector(0,lowerBound-5,0), color=color.blue, round=True, shaftwidth=.1))
y = (arrow(pos=vector(0,0,0), axis=vector(0,0,upperBound+5), color=color.green, round=True, shaftwidth=.1), arrow(pos=vector(0,0,0), axis=vector(0,0,lowerBound-5), color=color.green, round=True, shaftwidth=.1))

# delta t
detailP = .01
# change in x/y when graphing
detailG = .25

# MISC Functions

def formatInput(text):
    # Trig
    text = text.replace("arccos","acos")
    text = text.replace("cos^-1","acos")
    text = text.replace("arcsin","asin")
    text = text.replace("sin^-1","asin")
    text = text.replace("arctan","atan")
    text = text.replace("tan^-1","atan")

    # Power
    text = text.replace("^","**")
    
    return text

def ln(num):
    return log(num)/log(e)

# Parametric functions

xFuncG = ["","",""]
def setX1():
    global xFuncG
    xFuncG[0] = formatInput(xInput1.text)
def setX2():
    global xFuncG
    xFuncG[1] = formatInput(xInput2.text)
def setX3():
    global xFuncG
    xFuncG[2] = formatInput(xInput3.text)

yFuncG = ["","",""]
def setY1():
    global yFuncG
    yFuncG[0] = formatInput(yInput1.text)
def setY2():
    global yFuncG
    yFuncG[1] = formatInput(yInput2.text)
def setY3():
    global yFuncG
    yFuncG[2] = formatInput(yInput3.text)


zFuncG = ["","",""]
def setZ1():
    global zFuncG
    zFuncG[0] = formatInput(zInput1.text)
def setZ2():
    global xFuncG
    zFuncG[1] = formatInput(zInput2.text)
def setZ3():
    global xFuncG
    zFuncG[2] = formatInput(zInput3.text)

everythingEver = []
oldLine = [[],[],[]]
oldGraph = []
oldPoints = [[],[],[]]

def clear():
    for i in everythingEver:
        i.visible = False

def generateParametric(n):
    global oldLine
    for i in oldLine[n]:
        i.visible = False
    for i in oldPoints[n]:
        i[0].visible = False
        i[1].visible = False
    wack = vector(random.random(),random.random(),random.random())
    t = lowerBound
    xFunc = xFuncG[n]
    yFunc = yFuncG[n]
    zFunc = zFuncG[n]
    xLast = eval(xFunc)
    yLast = eval(yFunc)
    zLast = eval(zFunc)
    t = lowerBound+detailP
    c = curve(radius=0.1, color=wack)
    c.append(vector(xLast, zLast, yLast))
    parts = []
    while(t <= upperBound):
        # build xPos, yPos, zPos
        x = eval(xFunc)
        y = eval(yFunc)
        z = eval(zFunc)
        c.append(vector(x, z, y))
        everythingEver.append(c)
        xLast = x
        yLast = y
        zLast = z
        t+=detailP
    x = eval(xFunc)
    y = eval(yFunc)
    z = eval(zFunc)
    a = arrow(pos=vector(xLast,zLast,yLast), axis=vector(x-xLast,z-zLast,y-yLast), length=0.5, round=True, shaftwidth=0.2,headwidth=.4,headlength=.6,color=wack)
    parts.append(a)
    everythingEver.append(a)
    # write function text
    t = (lowerBound+upperBound)/2
    l = label(text="<%s, %s, %s>" % (xFunc, yFunc, zFunc), align="center", pos=vector(eval(xFunc),eval(zFunc),eval(yFunc)), color = wack)
    parts.append(l)
    everythingEver.append(l)
    parts.append(c)
    everythingEver.append(c)
    oldLine[n] = parts
    return parts

def parametricPoint(n):
    color = vector(random.random(),random.random(),random.random())
    c = (float)(eval(point[n].text))
    xFunc = sympify(xFuncG[n])
    yFunc = sympify(yFuncG[n])
    zFunc = sympify(zFuncG[n])
    t = symbols("t")
    x = N(xFunc.subs(t,c))
    y = N(yFunc.subs(t,c))
    z = N(zFunc.subs(t,c))
    pointLabel = (points(pos=[vector(x,z,y)],color=color, size_units="world",radius=.35),label(text="(%s, %s, %s)" % (f'{round(x,3):.2f}',f'{round(y,3):.2f}',f'{round(z,3):.2f}'), pos=vector(x,z,y),align="center", color=color))
    everythingEver.append(pointLabel[0])
    everythingEver.append(pointLabel[1])
    oldPoints[n].append(pointLabel)
    return pointLabel

# Plane/Object Functions
func = ""
def setGraph():
    global func
    global loading
    funny = formatInput(graphInput.text)
    try:
        funny.index("z")
        scene.title = "LOADING"
        loading = True
        z = symbols("z")
        f = sympify(funny)
        funny = solve(f,z).args[0]
        loading = False
        func = funny
        scene.title = ""
    except Exception as e:
        loading = False
        funny = sympify(funny)
        func = funny
    print(func)
    

def graphFunction():
    global loading
    global oldGraph
    if(not loading and func=="0"):
        for i in oldGraph:
            i.visible = False
    elif(not loading):
        for i in oldGraph:
            i.visible = False
        loading = True
        try:
            total = str(int(((abs(lowerBound)+abs(upperBound))/detailG)**2))
            scene.title = "LOADING"
            verticies = []
            # Start at x lower bound, move by detail to towards x upper bound, make quad describing the plane
            i = lowerBound
            j = lowerBound
            colorFunc = sympify("(atan(x/10)+3.14/2)/3.14")
            x,y = symbols("x y")

            rounds = 0
            while(i <= upperBound-detailG):
                try:
                    f1 = func.subs(x, i)
                    f2 = func.subs(x, i+detailG)
                    z1 = f1.subs(y,j)
                    z2 = f2.subs(y,j)
                    a = vertex(pos=vector(i,z1,j))
                    b = vertex(pos=vector(i+detailG,z2,j))
                    while(j <= upperBound-detailG):
                        try:
                            # print("(%s, %s)" % (i,j))
                            z3 = f1.subs(y, j+detailG)
                            z4 = f2.subs(y, j+detailG)
                            avg = abs(float((z1+z2+z3+z4)/2))
                            if(avg <= abs(upperBound*5)):
                                color = vector(colorFunc.subs(x,avg),0,0)
                                c = vertex(pos=vector(i,z3,j+detailG), color = color)
                                d = vertex(pos=vector(i+detailG,z4,j+detailG), color = color)
                                a.color = color
                                b.color = color
                                verticies.append(a)
                                verticies.append(b)
                                verticies.append(d)
                                verticies.append(c)
                                a = c
                                b = d
                            z1 = z3
                            z2 = z4
                        except Exception as e:
                            pass
                        j += detailG
                        rounds+=1
                        scene.title = "LOADING: %s/%s" % (rounds,total)
                except:
                    pass
                i += detailG
                j = lowerBound
            quads = []
            for i in range(0,len(verticies),4):
                Q = quad(vs=[verticies[i],verticies[i+1],verticies[i+2],verticies[i+3]])
                quads.append(Q)
            loading = False
            scene.title = ""
            final = quads
            oldGraph = quads
            return final
        except Exception as e:
            print(e)
            print("INVALID INPUT FOR GRAPH!")
            scene.title = ""
            loading = False
def setDetail():
    global detailG
    detailG = float(detailSet.text)
def setStart():
    global lowerBound
    old = lowerBound
    lowerBound = int(start.text)
    if(old != lowerBound):
        generateParametric(0)
        generateParametric(1)
        generateParametric(2)
def setEnd():
    global upperBound
    old = upperBound
    upperBound = int(end.text)
    if(old != upperBound):
        generateParametric(0)
        generateParametric(1)
        generateParametric(2)
def para1(): generateParametric(0)
def parap1(): parametricPoint(0)
def para2(): generateParametric(1)
def parap2(): parametricPoint(1)
def para3(): generateParametric(2)
def parap3(): parametricPoint(2)
scene.background=color.white
point = ["","",""]
scene.caption="Very cool 3D calculator <br>Bounds: "
start = winput(pos=scene.caption_anchor, bind=setStart, text="-10")
end = winput(pos=scene.caption_anchor, bind=setEnd, text="10")
scene.append_to_caption("<br>Graph Detail: ")
detailSet = winput(pos=scene.caption_anchor, bind=setDetail, text = "0.25")
scene.append_to_caption("<br>Set X function, Set Y function, Set Z function, Make point at t<br>Line input 1:")
xInput1 = winput(pos=scene.caption_anchor, bind=setX1)
yInput1 = winput(pos=scene.caption_anchor, bind=setY1)
zInput1 = winput(pos=scene.caption_anchor, bind=setZ1)
button(pos=scene.caption_anchor, bind=para1, text="Submit")
point[0] = winput(pos=scene.caption_anchor, bind=parap1)
scene.append_to_caption("<br>Line input 2: ")
xInput2 = winput(pos=scene.caption_anchor, bind=setX2)
yInput2 = winput(pos=scene.caption_anchor, bind=setY2)
zInput2 = winput(pos=scene.caption_anchor, bind=setZ2)
button(pos=scene.caption_anchor, bind=para2, text="Submit")
point[1] = winput(pos=scene.caption_anchor, bind=parap2)
scene.append_to_caption("<br>Line input 3: ")
xInput3 = winput(pos=scene.caption_anchor, bind=setX3)
yInput3 = winput(pos=scene.caption_anchor, bind=setY3)
zInput3 = winput(pos=scene.caption_anchor, bind=setZ3)
button(pos=scene.caption_anchor, bind=para3, text="Submit")
point[2] = winput(pos=scene.caption_anchor, bind=parap3)
scene.append_to_caption("<br>Graph input: ")
graphInput = winput(pos=scene.caption_anchor, bind=setGraph)
button(pos=scene.caption_anchor, bind=graphFunction, text="Submit")
scene.append_to_caption("<br>Clear broken things: ")
button(pos=scene.caption_anchor, bind=clear, text="Clear")

while True:
    rate(60)