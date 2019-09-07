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
		self.setupScreen()#runs the setupScreen method
		self.buttons()
		self.__root.mainloop()
	def setupScreen(self):
		self.__coolblue="#46ACC2"
		self.__canvas = tkinter.Canvas(master = self.__root, width = 500, height = 500)#creates a TKINTER canvas, not
		#a turtle one, with specifications 500*500. Possible TODO - make the screen size scale to the user's pc using winfo.getwidth?
		self.__sideBarCanvas=tkinter.Canvas(master=self.__root,width=66,height=500,bg=self.__coolblue,highlightthickness=0)
		self.__sideBarCanvas.grid(row=0,column=0,rowspan=500)
		self.__canvas.grid(column=1,row=0,columnspan=20,rowspan=125)#puts the canvas on the grid, in the window
		self.__screen = turtle.RawTurtle(self.__canvas)#now creates a RawTurtle class instance, which makes a window
		self.__pen2=turtle.RawTurtle(self.__canvas)
		self.__pen2.speed(0)
		#self.__pen2.hideturtle()
		self.__pen2.color("blue")
		self.__pen2.shape("circle")
		self.__pen2.turtlesize(stretch_wid=0.2,stretch_len=0.2) 
		self.__pen2.goto(-1,0)
		#a pen, but we can use it to draw the axes
		self.__screen.hideturtle()#Hides the pen. It's at the centre of the screen right now
		self.drawAxis()#code taken from the DrawsGraphs
	def manual(self):
		print ("manual pressed")
		webbrowser.open("manual.html",new=2)
		#self.__manualString="""Graphical representation and regression analysis program.\nManual\n\n1: Colour Changer\nThe icon with three colours in circles can be used to change the colour of the pen. Click it, and type in a colour. A list of valid colours names can be found by clicking the button at the bottom.\n\n2: Regression Analysis\nThis button will allow you to enter a set of values and have an approximate line of best fit drawn, using the least-squares regression method. Upon clicking the button, you will be prompted to enter how many values there are in your set of x/y co-ordinates. For example, if you have the set (1,1),(2,2),(3,3) then you must enter 3 here, because you have 3 sets of values. Then, press ENTER on your keyboard or click "OK" and enter the values in order in the table, as integer values. Decimals are not currently supported - as it is an approximation anyway, scale all your values up by the same factor, or round the values. When you have entered all the values, press OK or press ENTER again. The line should then be drawn. Currently, only linear graphs can be done accurately - polynomials will be undoubtedly innaccurate.\n\n3: Enter Equation\nThe third button, resembling a π symbol with a small plus, will allow you to enter a quadratic or linear equation and have it draw. Currently, only quadratics and linear equations are supported, and should be entered in the format "x^2+3x+5". The "a" value is taken to be 1 in this example, but can be entered as any value. An exampe of a linear would be "5x+5"\n\n4: Clear Canvas\nThe recycling bin button can be used to clear the canvas, and make it blank white again. Be careful not to click this one by accident!\n\n5: Information\nClicking this button will open the manual you are currently reading."""
		#self.__manual=tkinter.Toplevel(self.__root)
		#self.__manualText=tkinter.Label(self.__manual,text=self.__manualString,wraplength=750,justify="left",font=("Helvetica",12)).grid(row=0)
		
		#self.__manualColourListButton = tkinter.Button(self.__manual,text="Colour List",command=self.coloursList)
		#self.__manualColourListButton.grid(row=1,column=0,sticky="W")
		#self.__manualConfirm=tkinter.Button(self.__manual,text="Close",command=lambda:self.__manual.destroy())
		#self.__manualConfirm.grid(row=1,column=0,sticky="E")	
	def coloursList(self):#this subroutine will create a window that displays every "named" colour available for use in tkinter
		colours = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace','linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff','navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender','lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray','light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue','slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue','dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue','light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise','cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green','dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green','lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green','forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow','light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown','indian red', 'saddle brown', 'sandy brown','dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange','coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink','pale violet red', 'maroon', 'medium violet red', 'violet red','medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple','thistle', 'snow2', 'snow3','snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2','AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2','PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4','LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3','cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4','LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3','MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3','SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4','DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2','SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4','SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2','LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3','SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3','LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4','LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2','PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3','CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3','cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4','aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3','DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2','PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4','green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4','OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2','DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4','LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4','LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4','gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4','DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4','RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2','IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1','burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1','tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2','firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2','salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2','orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4','coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2','OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4','HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4','LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1','PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2','maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4','magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1','plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3','MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4','purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2','MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4','gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10','gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19','gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28','gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37','gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47','gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56','gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65','gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74','gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83','gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92','gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']#this list was taken from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter , creative commons license applies
		row = 0#not bothering with private variables as none of this is used anywhere else in the program so it can all be "deleted" outside this subroutine
		column = 0 #the list of colours is a long list of string colour names, row and column are used for positional gridding and start as 0
		self.__colourToplevel = tkinter.Toplevel(self.__root)#a toplevel window is created
		for colour in colours:#iterate through the for loop, taking each string
			temp = tkinter.Label(self.__colourToplevel,text=colour,background=colour)#a temp label where the text and colour are the colours from the list above current being iterated on
			temp.grid(row=row,column=column,sticky="ew")#grid that, with the row and column as its row and column, and sticky east-west to make it fill the "boxes" that it occupies when gridded.
			row = row+1#adds 1 to row, so the next item is gridded on the next row
			if row>30:#if the row is over 30, then it's time to start a new column
				row=0#row is set to 0 again
				column=column+1#column is increased

	def drawAxis(self):
		self.__screen.speed(0)#speed is instant
		self.__screen.penup()
		self.__screen.goto(-250,0) #The graphs axes are drawn with a 500x500 resolution
		self.__screen.pendown()
		self.__screen.goto(250,0)
		self.__screen.penup()
		self.__screen.goto(-1,-250)
		self.__screen.pendown()
		self.__screen.goto(-1,250)
		self.__screen.penup()
		self.__screen.goto(3,1);self.__screen.write("(0,0)")#writes lil numbers on the axes to let 	
		self.__screen.goto(3,238);self.__screen.write("(0,250)")#the user know what's poppin	
		self.__screen.goto(-248,0);self.__screen.write("(250,0)")
		self.__screen.goto(3,-248);self.__screen.write("(0,-250)")
		self.__screen.goto(215,0);self.__screen.write("(250,0)")
		self.__screen.goto(90,-250);self.__screen.write("Created by Tom Birkbeck and Callum Cafferty",font=("Helvetica",6))
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
	def clearCanvas(self):
		self.__pen2.clear()
		self.__pen2.penup()
		self.__pen2.goto(-1,0)
	def buttons(self):
		path=os.path.dirname(os.path.realpath(__file__))
		path2=path+"\Icons"
		self.__iconlist=[]
		for i in os.listdir(path2):
			print (i)
			x=Image.open("Icons/"+str(i)).resize((64,64),Image.ANTIALIAS).convert("RGBA")
			img=Image.new("RGBA",(64,64),(0,0,0,0))
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
		self.__canvasButton = tkinter.Button(self.__root,image=self.__canvasIcon,width=64,height=64,command=self.canvasButtonCallback, highlightthickness=0, bd=0, bg=self.__coolblue, activebackground=self.__coolbluedark)#a button to change the colour of the turtle
		self.__canvasButton.grid(row=0,column=0, sticky="n",pady=0)
		self.__equationButton = tkinter.Button(self.__root,image=self.__equationIcon,command=self.userEnterValues, highlightthickness=0, bd=0,width=64,height=64, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__equationButton.grid(row=1,column=0, sticky="n",pady=0)
		self.__manualButton=tkinter.Button(self.__root,image=self.__manualIcon,command=self.manual, highlightthickness=0, bd=0,width=64,height=64, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__manualButton.grid(row=124, sticky="s",pady=0)
		self.__dataButton = tkinter.Button(self.__root,image=self.__tableIcon,command=self.tableInsert, highlightthickness=0, bd=0,width=64,height=64, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__dataButton.grid(row=2,column=0, sticky="n",pady=0)
		self.__clearButton = tkinter.Button(self.__root,image=self.__clearIcon,command=self.clearCanvas, highlightthickness=0, bd=0,width=64,height=64, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__clearButton.grid(row=3, sticky="n",pady=0)
		
	def canvasButtonCallback(self): #a subroutine for changing the colour of the pen
		#self.__colourinwindow=tkinter.Toplevel(self.__root)
		#self.__colourinwindow.bind("<Return>",self.colour)
		#self.__colourinwindow.lift()
		#self.__colourinwindow.title("Colour input")#Creates a new window with title colour input
		#self.__colourlbl=tkinter.Label(master=self.__colourinwindow, text="Please enter your chosen colour as a colour name or hex code").grid(row=0) #Adds a label to tell the user how to input colours
		#self.__colourin=tkinter.Entry(master=self.__colourinwindow) #Creates an entry field 
		#self.__colourin.focus_set() #Automatically sets the user's keyboard 
		#self.__colourin.grid(row=1) #Puts the entry into a row
		#self.colourinbutton=tkinter.Button(master=self.__colourinwindow, text="OK", command=lambda:self.colour(None)).grid(row=3) #Adds a confirm button for the colour input, which calls the colour subroutine
		#if self.__colourin=="":
		#	self.__colourin="black"
		print ("color pressed")
	def colour(self,Event):
		try:
			self.__pen2.pencolor(self.__colourin.get()) #Sets the colour to whatever the user inputted
			
			self.__colourinwindow.destroy()
		except:
			self.__colourinwindow.destroy()#If the colour inputted by the user isn't either a hex code or a colour name...
			#errorWindow = tkinter.Toplevel(self.__root)
			#errorLabel=tkinter.Label(errorWindow,text="Error\nInvalid colour, please try again").grid() #an error message is shown
			self.colourButtonCallback()
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
instance = Application(tkinter.Tk())
