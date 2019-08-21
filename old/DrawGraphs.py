#GraphsQuadratics
import turtle
import math
pen1=turtle.Turtle()
pen1.speed(0) #Means stuff will immidiately draw when possible as opposed to "waiting"
pen2=turtle.Turtle()
pen2.speed(0)
screen=turtle.Screen()
screen.bgcolor("white")
equation = "3x+4"
def analyseEquation(equation):
    a="0"
    b="0"
    c="0"
    xsqr=False
    lin=False
    if not "^" in equation:
        xsqr=True
        lin=True
    equation=list(equation) #Converts the equation text to a list of characters bc it's easier to work with
    for i in range (0, len(equation)):
        if equation[i]=="x" and xsqr==False:
            xsqr=True
            if equation[i+1]=="^":
                a=""
                for j in range (0,i):
                    a=a+(equation[j]) #Finds the first occurance of x^2, and sets a to all the numbers preceding it
                if i==0:
                    a="1"   #If there are no values before x^2, a is set to 1
            else:
                pass
        elif equation[i]=="x" and xsqr==True:
            b=""
            xpos=i
            if "+" in equation:
                for k in range (equation.index("+"), i):
                    b=b+(equation[k])   #Finds the first occurance of x, and sets b to all the numbers preceding it
                if i==0:
                    b="1" # #If there are no values before x, b is set to 1
            if "-" in equation:
                if xsqr==True and equation.index("-")==0:
                    equation[equation.index("-")]="何"
                for k in range (equation.index("-"), i):
                    b=b+(equation[k])   #Finds the first occurance of x, and sets b to all the numbers preceding it
                if i==0:
                    b="1" # #If there are no values before x, b is set to 1
            if lin==True:
                for k in range (0, i):
                    b=b+(equation[k])   #Finds the first occurance of x, and sets b to all the numbers preceding it
                if i==0:
                    b="1"
        elif i==(len(equation)-1) and not equation[i]=="x" and not equation[i-1]=="^":
            c=""
            for s in range (xpos+1, len(equation)):
                c=c+(equation[s]) #Finds whatever has been added at the end of the equation
    return (float(eval(a))),(float(eval(b))),(float(eval(c))),lin
def getTurningPoint():#The turning point is returned from the formula -b/2a
    a,b,c,lin = analyseEquation(equation)
    if lin==True:
        pass
    else:
        x=((-b)/(2*a))
        y=(a*(x**2))+(b*x)+c        
        return x,y
def getMaxPoint():
    a,b,c,lin = analyseEquation(equation)
    if lin==True:
        pass
    else:
        try:
            maxPointA=round((-b+(math.sqrt((b**2)-(4*a)*(c-250))))/(2*a))
            maxPointB=round((-b-(math.sqrt( b**2-4*a*(c-250) )))/(2*a))
        except:
            maxPointA=round((-b+(math.sqrt((b**2)-(4*a)*(c+250))))/(2*a))
            maxPointB=round((-b-(math.sqrt( b**2-4*a*(c+250) )))/(2*a))
    if maxPointA>maxPointB:
        difference=maxPointA-maxPointB
    else:
        difference=maxPointB-maxPointA
    return maxPointA,maxPointB,difference
def drawAxis():
    pen1.penup()
    pen1.goto(-250,0) #The graphs axes are drawn with a 250x250 resolution
    pen1.pendown()
    pen1.goto(250,0)
    pen1.penup()
    pen1.goto(0,-250)
    pen1.pendown()
    pen1.goto(0,250)
def drawGraph():
    a,b,c,lin=analyseEquation(equation)
    x=(getMaxPoint()[1]) #The start point is determined using maxPointA, meaning the graph only draws within the screen boundary
    if lin==False:
        y=(a*(x**2))+(b*x)+c
    else:
        y=250
    if x>0:
        negativeStart=True
    if 0>x:
        negativeStart=False
    for i in range (0,(getMaxPoint()[2])): #Draws the graph by calculating the x and y values using the equation stated earlier
        pen2.penup()        #Calculates the y values 250 times, incrementing x by 1 each time
        pen2.goto(x,y)
        pen2.pendown()
        if negativeStart==False:
            x=x+1
        if negativeStart==True:
            x=x-1
        y=(a*x**2)+(b*x)+c 
        pen2.goto(x,y)
        print (x,y)
pen1.color("black") #Sets the axis color to black
pen2.color("blue") #Sets the graph color to blue
print ("a={0} b={1} c={2}".format(analyseEquation(equation)[0],analyseEquation(equation)[1],analyseEquation(equation)[2]))
if analyseEquation(equation)[3]==False:
    print ("Turning point is ({0},{1})".format(getTurningPoint()[0],getTurningPoint()[1]))
print (getMaxPoint()[0],getMaxPoint()[1],getMaxPoint()[2])
drawAxis()
drawGraph()