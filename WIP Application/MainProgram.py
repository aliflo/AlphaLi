#main program to "concatenate" all our code into, and slap a nice UI over the top

#TODO
#make it so when you open a window (e.g. a enter equation window) by clicking a button, if you clickt the button again it deosn't open another window but just brings the other window to the front
#move the menu icons off the actual canvas and give them a bar on the left
#change error handling for reading the table so if all values are error it just says all are wrong (rather than a huge list of error messages)
#TODO LONG TERM
#R class that does polynomial regression
#add support for linear and higher degree polynomial entry into the box
#scrolling/zooming in the canvas

import numpy as np
import turtle,tkinter,math,os,webbrowser
from PIL import Image, ImageTk, ImageFilter

class Application(tkinter.Frame):#calling with tkinter.Frame . would be just Frame if I had done "from tkinter import *",
#but the advantage of doing just import tkinter is that it's technically "cleaner" code as you don't risk possible 
#conflicts in large programs with many imports - e.g., your "neoMaths" mod also has function called Frame for some reason
	def __init__(self,master):#with self and master, and master will be the highest level widget
		tkinter.Frame.__init__(self,master)#creates a frame inside master; this makes shoving a turtle canvas in it easier
		self.__root = master#redefines master as self.__root so it can be used in other methods of this class
		self.__root.title("Graphing Program")
		self.grid()#puts the window in a grid  
		self.setupScreen(500,500,True)#runs the setupScreen method
		self.__root.mainloop()
	def setupScreen(self, w, h,init):
		self.__coolblue="#46ACC2"
		self.__canvas = tkinter.Canvas(master = self.__root, height = h, width = w)#creates a TKINTER canvas, not
		#a turtle one, with specifications 500*500. Possible TODO - make the screen size scale to the user's pc using winfo.getwidth?
		self.__sideBarCanvas=tkinter.Canvas(master=self.__root,width=63,height=h,bg=self.__coolblue,highlightthickness=0)
		self.__sideBarCanvas.grid(row=0,column=0,rowspan=h)
		self.__canvas.grid(column=1,row=0,columnspan=20,rowspan=125)#puts the canvas on the grid, in the window
		self.__screen = turtle.RawTurtle(self.__canvas)#now creates a RawTurtle class instance, which makes a window
		self.__pen2=turtle.RawTurtle(self.__canvas)
		self.__pen2.speed(0)
		#self.__pen2.hideturtle()
		self.__pen2.color("blue")
		self.__pen2.shape("circle")
		self.__pen2.turtlesize(stretch_wid=0.25,stretch_len=0.25) 
		self.__pen2.goto(-1,0)
		#a pen, but we can use it to draw the axes
		self.buttons(h,w,init)
		self.__screen.hideturtle()#Hides the pen. It's at the centre of the screen right now
		self.drawAxis(w,h)#code taken from the DrawsGraphs
	def manual(self):
		os.chdir(os.path.dirname(os.path.realpath(__file__)))
		print ("manual pressed")
		webbrowser.open("manual.html",new=2)	
	def drawAxis(self,x,y):
		self.__screen.speed(0)#speed is instant
		self.__screen.penup()
		self.__screen.goto(-x,0) #The graphs axes are drawn with a 500x500 resolution
		self.__screen.pendown()
		self.__screen.goto(x,0)
		self.__screen.penup()
		self.__screen.goto(-1,-y)
		self.__screen.pendown()
		self.__screen.goto(-1,y)
		self.__screen.penup()
		self.__screen.goto(3,1);self.__screen.write("(0,0)")#writes lil numbers on the axes to let 	
		self.__screen.goto(3,(y//2)-12);self.__screen.write("(0,"+str(y//2)+")")#the user know what's poppin	
		self.__screen.goto(-((x//2)-12),0);self.__screen.write("(-"+str(x//2)+",0)")
		self.__screen.goto(3,-((y//2)-12));self.__screen.write("(0-,"+str(y//2)+")")
		self.__screen.goto(((x//2)-48),0);self.__screen.write("("+str(x//2)+",0)")
		self.__screen.goto(90,-(y//2));self.__screen.write("Created by Tom Birkbeck and Callum Cafferty",font=("Helvetica",6))
	def right(self,event):
		if not event.widget in self.__tableCellsListYvalues:
			self.__tableCellsListYvalues[self.__tableCellsListXvalues.index(event.widget)].focus_set()			
	def left(self,event):
		if not event.widget in self.__tableCellsListXvalues:
			self.__tableCellsListXvalues[self.__tableCellsListYvalues.index(event.widget)].focus_set()
	def up(self,event):
		if event.widget in self.__tableCellsListXvalues:
			if self.__tableCellsListXvalues.index(event.widget)!=0:
				self.__tableCellsListXvalues[self.__tableCellsListXvalues.index(event.widget)-1].focus_set()
		else:
			if self.__tableCellsListYvalues.index(event.widget)!=0:
				self.__tableCellsListYvalues[self.__tableCellsListYvalues.index(event.widget)-1].focus_set()
	def down(self,event):
		if event.widget in self.__tableCellsListXvalues:
			if self.__tableCellsListXvalues.index(event.widget)!=(self.__tHeight-1):
				self.__tableCellsListXvalues[self.__tableCellsListXvalues.index(event.widget)+1].focus_set()
		else:
			if self.__tableCellsListYvalues.index(event.widget)!=(self.__tHeight-1):
				self.__tableCellsListYvalues[self.__tableCellsListYvalues.index(event.widget)+1].focus_set()
	def returnManager(self,event):
		if event.widget in self.__tableCellsListXvalues:
			if self.__tableCellsListXvalues.index(event.widget)==self.__tHeight-1:
				self.__tableCellsListYvalues[0].focus_set()
			else:
				self.__tableCellsListXvalues[self.__tableCellsListXvalues.index(event.widget)+1].focus_set()
		else:
			if self.__tableCellsListYvalues.index(event.widget)==self.__tHeight-1:
				self.__tableInput.focus_set()
			else:
				self.__tableCellsListYvalues[self.__tableCellsListYvalues.index(event.widget)+1].focus_set()
	def tableCreate(self):
		self.__tableInput.unbind("<Return>")
		self.__xLabel=tkinter.Label(self.__tableInput,text="x")#this just puts x at the top of the table we are about to define so the user knows what to type where
		self.__xLabel.grid(row=0,column=0)#grid the above
		self.__yLabel=tkinter.Label(self.__tableInput,text="y")
		self.__yLabel.grid(row=0,column=1)
		self.__tableCellsListXvalues = []#defining a list of cells for a table that we will use to let users enter values for regression analysis
		self.__tableCellsListYvalues = []
		for j in range (self.__tHeight):#the height of the table - aka how many individual x/y values the user inputs
			for i in range(2):#width of the table is 2 - basically means we take both x and y values and not just the x or just hte y
				self.__tableCell=tkinter.Entry(self.__tableInput)#temporary self.__tableCell is an Entry widget from Tkinter, a box for the user to fill with an x or y value
				self.__tableCell.bind("<Up>",self.up)
				self.__tableCell.bind("<Down>",self.down)
				self.__tableCell.bind("<Left>",self.left)
				self.__tableCell.bind("<Right>",self.right)
				self.__tableCell.bind("<Tab>",self.returnManager)

				self.__tableCell.grid(row=j+1,column=i)#grids the entry widget defined above. definition order is, according to the for loops, all of the x v
				if i==0:#
					self.__tableCellsListXvalues.append(self.__tableCell)
					self.__tableCell.config(bg="azure2")
				elif i==1:
					self.__tableCellsListYvalues.append(self.__tableCell)
					self.__tableCell.config(bg="azure3")
		self.__okButton = tkinter.Button(self.__tableInput,command=lambda:self.tableGet(None),text="Done")
		self.__tableCellsListXvalues[0].focus_set()
		self.__tableInput.bind("<Return>",self.tableGet)
		self.__okButton.grid(column=1,sticky="E" , row=self.__tHeight+1)#yeah
	def tableGet(self,event):#callback function for the okButton in tableCreate subroutine
		self.__dictionaryOfValues = {}#this dictionary will contain the values of the thingy in the format {x:y,x1:y1}
		for i in range (self.__tHeight):
			try:
				self.__dictionaryOfValues[int(self.__tableCellsListXvalues[i].get())] = int(self.__tableCellsListYvalues[i].get())
			except:
				print("Console: There was an error with the addition of row number {0} to the table of values; most likely you didn't use an integer value. This has been skipped.".format(i))
		if len(self.__dictionaryOfValues)==0:
			print("Console: All the values you entered were invalid. Please try again.")
			self.__tableInput.destroy()
		else:
			x = regressionAnalysisInstance(self.__dictionaryOfValues)
			#print(x.values[0])
			self.__equation = ("{0}x+{1}".format(x.values[1],x.values[0]))
			#print(self.__equation)
			instance = AnalyseEquation(self.__equation)
			#AnalyseEquation.returnValues(self)
			#print("A: {0}\nB: {1}\nC: {2}\nLin: {3}\nTpoint: {4}".format(instance.getA(),instance.getB(),instance.getC(),instance.getLinear(),instance.getCanvasBound()))
			self.__a = instance.getA()
			self.__b = instance.getB()
			self.__c = instance.getC()
			self.__lin = instance.getLinear()
			self.__canvasBound = instance.getCanvasBound()
			self.drawGraph()
			self.__tableInput.destroy()
		#print(self.__dictionaryOfValues)
	def itemNumConfirmCallback(self,Event):
		self.__tHeight=int(self.__itemNumEntry.get())
		self.__itemNumEntry.grid_forget()
		self.__itemNumLabel.grid_forget()
		self.__itemNumConfirm.grid_forget()
		self.tableCreate()
	def tableInsert(self):
		#self.__tableInput=tkinter.Toplevel()
		#self.__tableEntries={}
		#self.__itemNumEntry=tkinter.Entry(self.__tableInput)
		#self.__itemNumEntry.focus_set()
		#self.__itemNumEntry.grid(column=1, row=1)
		#self.__itemNumLabel=tkinter.Label(self.__tableInput,text="Please enter the number of items you wish to enter")
		#self.__itemNumLabel.grid(column=1, row=0)
		#self.__itemNumConfirm=tkinter.Button(self.__tableInput,text="Confirm",command=lambda:self.itemNumConfirmCallback(None))
		#self.__itemNumConfirm.grid(column=2, row=1)
		#self.__tableInput.bind("<Return>",self.itemNumConfirmCallback)
		print ("table button pressed")
		self.__pen2.goto(0,0)
		self.__pen2.circle(50)
	def userEnterValues(self):
		#user enters equation here
		#self.__equationWindow=tkinter.Toplevel()
		#self.__equationWindow.title("Enter an equation")
		#self.__equationEntry = tkinter.Entry(self.__equationWindow)
		#self.__equationEntry.focus_set()
		#self.__equationEntry.grid(row=21,column=10)
		#self.__equationWindow.bind("<Return>", self.defineEquation)
		#QOL change, enter sends the entry also instead of clicking button
		#self.__equationEntered = tkinter.Button(self.__equationWindow,text="Enter", command=lambda:self.defineEquation(None))
		#self.__equationEntered.grid(row=21,column=11)
		print ("equation button pressed")
		self.__canvas.scale("all",0,0,0.5,0.5)
	def clearCanvas(self):
		self.__pen2.clear()
		self.__pen2.penup()
		self.__pen2.goto(-1,0)
	def buttons(self,h,w,init):
		if init==False:
			self.__canvasButton.grid_forget()
			self.__equationButton.grid_forget()
			self.__manualButton.grid_forget()
			self.__dataButton.grid_forget()
			self.__clearButton.grid_forget()
		path=os.path.dirname(os.path.realpath(__file__))
		path2=path+"/Icons/"
		self.__iconlist=[]
		for i in sorted(os.listdir(path2)):
			x=Image.open(path2+str(i)).resize((62,62),Image.ANTIALIAS).convert("RGBA")
			img=Image.new("RGBA",(62,62),(0,0,0,0))
			img.paste(x, mask=x)
			img.filter(ImageFilter.SMOOTH_MORE)
			img.filter(ImageFilter.SMOOTH_MORE)
			self.__iconlist.append(img)
		self.__clearIcon=ImageTk.PhotoImage(self.__iconlist[0])
		self.__canvasIcon=ImageTk.PhotoImage(self.__iconlist[1])
		self.__equationIcon=ImageTk.PhotoImage(self.__iconlist[2])
		self.__tableIcon=ImageTk.PhotoImage(self.__iconlist[3])
		self.__manualIcon=ImageTk.PhotoImage(self.__iconlist[4])
		self.__coolblue="#46ACC2"
		self.__coolbluedark="#3b91a3"
		self.__canvasButton = tkinter.Button(self.__root,image=self.__canvasIcon,width=62,height=62,command=self.canvasButtonCallback, highlightthickness=0, bd=0, bg=self.__coolblue, activebackground=self.__coolbluedark)#a button to change the colour of the turtle
		self.__canvasButton.grid(row=0,column=0, sticky="n",pady=0)
		self.__equationButton = tkinter.Button(self.__root,image=self.__equationIcon,command=self.userEnterValues, highlightthickness=0, bd=0,width=62,height=62, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__equationButton.grid(row=1,column=0, sticky="n",pady=0)
		self.__manualButton=tkinter.Button(self.__root,image=self.__manualIcon,command=self.manual, highlightthickness=0, bd=0,width=62,height=62, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__manualButton.grid(row=124, sticky="s",pady=0)
		self.__dataButton = tkinter.Button(self.__root,image=self.__tableIcon,command=self.tableInsert, highlightthickness=0, bd=0,width=62,height=62, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__dataButton.grid(row=2,column=0, sticky="n",pady=0)
		self.__clearButton = tkinter.Button(self.__root,image=self.__clearIcon,command=self.clearCanvas, highlightthickness=0, bd=0,width=62,height=62, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__clearButton.grid(row=3, sticky="n",pady=0)
		#tooltip creation using CreateToolTip class as taken from daniweb
		#see bibliography (vegaseat, 2015)
		self.__clearButtonTTP=CreateToolTip(self.__clearButton, "Clear Canvas")
		self.__dataButtonTTP=CreateToolTip(self.__dataButton, "Data Analysis Menu")
		self.__manualButtonTTP=CreateToolTip(self.__manualButton, "Program Manual")
		self.__canvasButtonTTP=CreateToolTip(self.__canvasButton, "Canvas Manipulator")
		self.__equationButtonTTP=CreateToolTip(self.__equationButton, "Equation Entry")
	def colourWindow(self):
		self.__colours = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace','linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff','navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender','lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray','light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue','slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue','dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue','light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise','cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green','dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green','lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green','forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow','light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown','indian red', 'saddle brown', 'sandy brown','dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange','coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink','pale violet red', 'maroon', 'medium violet red', 'violet red','medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple','thistle', 'snow2', 'snow3','snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2','AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2','PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4','LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3','cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4','LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3','MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3','SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4','DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2','SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4','SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2','LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3','SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3','LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4','LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2','PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3','CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3','cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4','aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3','DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2','PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4','green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4','OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2','DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4','LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4','LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4','gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4','DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4','RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2','IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1','burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1','tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2','firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2','salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2','orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4','coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2','OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4','HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4','LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1','PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2','maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4','magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1','plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3','MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4','purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2','MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4','gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10','gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19','gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28','gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37','gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47','gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56','gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65','gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74','gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83','gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92','gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']#this list was taken from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter , creative commons license applies
		self.__colourinwindow=tkinter.Toplevel(self.__canvasWindow)
		row = 0
		column = 0
		for colour in self.__colours:#iterate through the for loop, taking each string
			temp = tkinter.Button(self.__colourinwindow,background=colour, bd=0, command=lambda x=colour: self.colour(x))#a temp label where the text and colour are the colours from the list above current being iterated on
			temp.grid(row=row,column=column,sticky="ew",padx=0,pady=0)#grid that, with the row and column as its row and column, and sticky east-west to make it fill the "boxes" that it occupies when gridded.
			row = row+1#adds 1 to row, so the next item is gridded on the next row
			if row>15:#if the row is over 30, then it's time to start a new column
				row=0#row is set to 0 again
				column=column+1#column is increased
	def resizeCallback(self):
		self.__canvas.grid_forget()
		self.__sideBarCanvas.grid_forget()
		self.setupScreen(int(self.__resizeXEntry.get()),int(self.__resizeYEntry.get()),False)
	def canvasButtonCallback(self): #a subroutine for changing the colour of the pen
		self.__canvasWindow=tkinter.Toplevel(self.__root)
		self.__canvasWindow.title("Canvas")
		self.__colorLabel=tkinter.Label(self.__canvasWindow, text="Colour:").grid(row=0, column=0, padx=5, pady=10,sticky="w")
		self.__colorButton=tkinter.Button(self.__canvasWindow,highlightthickness=0,background=self.__pen2.color()[0], activebackground=self.__pen2.color()[0], command=self.colourWindow)
		self.__colorButton.grid(row=0, column=1, padx=2, pady=(0,5),sticky="w")
		self.__resizeButton=tkinter.Button(self.__canvasWindow, text="Resize",command=self.resizeCallback)
		self.__resizeButton.grid(row=3,column=1,padx=2, pady=(5,0))
		self.__resizeXlabel=tkinter.Label(self.__canvasWindow,text="Width:").grid(row=1,column=0,padx=2,pady=2, sticky="w")
		self.__resizeYlabel=tkinter.Label(self.__canvasWindow,text="Height:").grid(row=2,column=0,padx=2,pady=2, sticky="w")
		self.__resizeXEntry=tkinter.Entry(self.__canvasWindow, width=4)
		self.__resizeXEntry.insert(0,str(self.__canvas.winfo_width()-2))
		self.__resizeXEntry.grid(row=1,column=1,padx=2,pady=2,sticky="w")
		self.__resizeYEntry=tkinter.Entry(self.__canvasWindow,width=4)
		self.__resizeYEntry.insert(0,str(self.__canvas.winfo_height()-2))
		self.__resizeYEntry.grid(row=2,column=1,padx=2,pady=2,sticky="w")
		self.__cancelButton=tkinter.Button(self.__canvasWindow, text="Cancel", command=lambda: self.__canvasWindow.destroy())
		self.__cancelButton.grid(row=3, column=0, padx=2, pady=(5,0))
		self.__canvasWindow.grid()
	def colour(self,colour):
		self.__pen2.pencolor(colour)
		self.__colourinwindow.destroy()
		self.__canvasWindow.destroy()
		self.canvasButtonCallback()
	def defineEquation(self,event):
		self.__equation = self.__equationEntry.get()
		self.__equationWindow.destroy()
		instance = AnalyseEquation(self.__equation)
		#AnalyseEquation.returnValues(self)
		#print("A: {0}\nB: {1}\nC: {2}\nLin: {3}\nTpoint: {4}".format(instance.getA(),instance.getB(),instance.getC(),instance.getLinear(),instance.getCanvasBound()))
		self.__a = instance.getA()
		self.__b = instance.getB()
		self.__c = instance.getC()
		self.__lin = instance.getLinear()
		self.__canvasBound = instance.getCanvasBound()
		self.__canvasBoundLength=instance.getCanvasBoundLength()
		self.drawGraph()
	def drawGraph(self):
		x=(self.__canvasBound) #The start point is determined using maxPointA, meaning the graph only draws within the screen boundary
		if self.__lin==False:
			if self.__a<1:
				self.__pen2.ht()
			y=(self.__a*(x**2))+(self.__b*x)+self.__c
			if x>0:
				negativeStart=True
			if 0>x:
				negativeStart=False
			for i in range (0,(self.__canvasBoundLength+1)): #Draws the graph by calculating the x and y values using the equation stated earlier
				self.__pen2.penup()        #Calculates the y values 250 times, incrementing x by 1 each time
				self.__pen2.goto(x,y)
				self.__pen2.pendown()
				y=(self.__a*x**2)+(self.__b*x)+self.__c
				if negativeStart==False:
					x=x+1
				if negativeStart==True:
					x=x-1
				self.__pen2.goto(x,y)
			self.__pen2.st()
		else:
			self.__pen2.penup()
			x=-250
			y=self.__b*x+self.__c
			self.__pen2.goto(x,y)
			self.__pen2.pendown()
			x=250
			y=self.__b*x+self.__c
			self.__pen2.goto(x,y)



class CreateToolTip(object): #(vegaseat, 2015) see bibliography
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 65
        y += self.widget.winfo_rooty() + 50
        # creates a toplevel window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.tw, text=self.text, justify='left',
                       background='grey', relief='solid', borderwidth=0, fg="white",
                       font=("helvetica", "10", "normal",))
        label.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()

instance = Application(tkinter.Tk())
