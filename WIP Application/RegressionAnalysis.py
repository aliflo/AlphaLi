#hi there. these functions probably won't work if you just want to rip them and plug them in the main program right now.
#will fix all that shite later.
import numpy as np#need to pip this shit. for clarity, it's not numpy, it's NumPy as in Number Python. Confused me too - who the fuck names a module numpy?
import turtle
class analysisInstance:
	def __init__(self,values):
		#for now, just using a test set of values. will eventually pull from a spreadsheet.
		self.__values = values#should be saved as a dictionary, of x:y values.
		"""we can derive y=mx+c from normal equations
		notes on the so called normal equations:
		sum of all the y values = number of values*c + m*sum of all x values
		sum of the set of x*y = c*sum of x values + m*sum of x^2 values
		This seems a little complicated in comment form in python. Equations make more sense written!"""
		#so with our values, we can find the sum of all x values, sum of all y values, sum of x^2 values and the sum of xy values.
		self.setValues()
		print("""Sum of the x values: {0} {5}
Sum of the y values: {1} {6}
Sum of the x*y values: {2} {7}
Sum of the x^2 values: {3} {8}
Total number of values: {4} {9}""".format(self.__sumX,self.__sumY,self.__sumXY,self.__sumXSquared,self.__n,type(self.__sumX),type(self.__sumY),type(self.__sumXY),type(self.__sumXSquared),type(self.__n)))
		self.solveEquations()
	def setValues(self):
		self.__sumX = 0
		self.__sumY = 0
		self.__sumXY = 0
		self.__sumXSquared = 0
		self.__n = 0
		for x,y in self.__values.items():
			xy = x*y
			xsquared = x*x
			self.__sumXSquared+=xsquared
			self.__sumXY+=xy
			self.__sumX+=x
			self.__sumY+=y
			self.__n+=1
	def solveEquations(self):
		localN = self.__n
		#this lil doodad, using new thingymabob called numpy, converts it into a matrix to solve as simultaneous equations.
		#confusing - this tutorial does better explain that me. http://dwightreid.com/blog/2015/09/21/python-how-to-solve-simultaneous-equations/
		A = np.array([[self.__n,self.__sumX],[self.__sumX,self.__sumXSquared]])
		B = np.array([self.__sumY,self.__sumXY])
		self.__C = np.linalg.solve(A,B)
	@property
	def values(self):
		return self.__C[0],self.__C[1]#c and m, respectively.
instance = analysisInstance({1:2,2:4})
c,m=instance.values
def drawGraph(c,m):
	#graph: y=mx+c
	screen = turtle.Screen()
	pen1 = turtle.Turtle()
	pen1.speed(0)
	drawAxis(pen1)
#################################################
	#y = m*x+c
	pen1.color("blue")
	pen1.up()
	pen1.goto(-500,-500)
	#low point:
	lowPointY = (m*-500)+c
	pen1.goto(-500,lowPointY)
	##high point:
	highPointY = (m*500)+c
	pen1.down()
	pen1.goto(500,highPointY)
	count = []
	for i in range(-500,500):
		if -1<m*i+c<1:
			count.append(i)
	countSum = 0
	for each in count:
		countSum+=each
	countAvg = countSum/len(count)
	print(countAvg)
	pen1.up()
	pen1.goto(countAvg,500)

def drawAxis(pen1):
	pen1.speed(0)#speed is instant
	pen1.penup()
	pen1.goto(-600,0) #The graphs axes are drawn with a 600x600 resolution
	pen1.pendown()#why are they drawn 600x600? the screen size on the other program is also 500x500, so I was a little confused by this.
	pen1.goto(600,0)
	pen1.penup()
	pen1.goto(0,-600)
	pen1.pendown()
	pen1.goto(0,600)
	pen1.penup()
	pen1.goto(3,1);pen1.write("(0,0)")#writes lil numbers on the axes to let 	
	pen1.goto(3,238);pen1.write("(0,250)")#the user know what's poppin	
	pen1.goto(-248,0);pen1.write("(250,0)")
	pen1.goto(3,-248);pen1.write("(0,-250)")
	pen1.goto(215,0);pen1.write("(250,0)")
drawGraph(c,m)
