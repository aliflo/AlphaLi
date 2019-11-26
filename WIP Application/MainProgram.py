import numpy as np
import turtle,tkinter,math,os,webbrowser,subprocess,re,csv,tkinter.font,sympy,tkinter.filedialog
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
		self.__h,self.__w=h,w
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
		self.__pen2.goto(0,0)
		self.__pen2.ht()
		#a pen, but we can use it to draw the axes
		self.buttons(h,w,init)
		self.__screen.hideturtle()#Hides the pen. It's at the centre of the screen right now
		self.drawAxis(w,h)#code taken from the DrawsGraphs
		self.addLabels(w,h,w,h)
	def manual(self):
		os.chdir(os.path.dirname(os.path.realpath(__file__)))
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
		self.__screen.goto(90,-(y//2));self.__screen.write("Created by Tom Birkbeck and Callum Cafferty",font=("Helvetica",6))
	def addLabels(self,x,y,ax,ay):
		self.__screen.goto(3,1);self.__screen.write("(0,0)")#writes lil numbers on the axes to let 	
		self.__screen.goto(3,(ay//2)-12);self.__screen.write("(0,"+str(y//2)+")")#the user know what's poppin	
		self.__screen.goto(-((ax//2)-12),0);self.__screen.write("(-"+str(x//2)+",0)")
		self.__screen.goto(3,-((ay//2)-12));self.__screen.write("(0-,"+str(y//2)+")")
		self.__screen.goto(((ax//2)-48),0);self.__screen.write("("+str(x//2)+",0)")
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
			self.__equation = ("{0}x+{1}".format(x.values[1],x.values[0]))
			instance = AnalyseEquation(self.__equation)
			#AnalyseEquation.returnValues(self)
			self.__a = instance.getA()
			self.__b = instance.getB()
			self.__c = instance.getC()
			self.__lin = instance.getLinear()
			self.__canvasBound = instance.getCanvasBound()
			self.drawGraph()
			self.__tableInput.destroy()
	def itemNumConfirmCallback(self,Event):
		self.__tHeight=int(self.__itemNumEntry.get())
		self.__itemNumEntry.grid_forget()
		self.__itemNumLabel.grid_forget()
		self.__itemNumConfirm.grid_forget()
		self.tableCreate()
	def dataMenu(self):
		self.__dataMenu=tkinter.Toplevel(self.__root,bg=self.__coolbluedark)
		self.__dataMenu.title("Data Menu")
		self.__dataMenu.grid()
		#self.__dataMenu["bg"]=self.__coolblue
		self.__dataMenuFrame = tkinter.Frame(self.__dataMenu,bg=self.__coolbluedark,height=250,width=160)
		self.__WHOButton = tkinter.Button(self.__dataMenuFrame,image=self.__mosquitoIcon,command=self.WHOdata,height=64,width=64,)
		self.__AIButton=tkinter.Button(self.__dataMenuFrame,command=self.AIdata,image=self.__AIICon,height=64,width=64)
		self.__UserDataButton=tkinter.Button(self.__dataMenuFrame,command=self.UserData,image=self.__uploadIcon,height=64,width=64)
		
		self.__dataMenuFrame.grid(row=0,column=0,sticky="EW")
		self.__dataMenuFrame.grid_columnconfigure(0, weight=1)
		self.__dataMenuFrame.grid_columnconfigure(2, weight=1)
		self.__dataMenuFrame.grid_rowconfigure(1,weight=1)
		self.__dataMenuFrame.grid_rowconfigure(3,weight=1)
		
		self.__dataMenuFrame.grid_propagate(False)
		self.__WHOButton.grid(row=0,column=1,sticky="E")
		self.__AIButton.grid(row=2,column=1,sticky="E")
		self.__UserDataButton.grid(row=4,column=1,sticky="E")

		self.__WHOButtonTTP=CreateToolTip(self.__WHOButton, "World Health Organisation data, charting malaria cases in various nations from 2011-2017.\nSourced from https://www.who.int/gho/malaria/epidemic/cases/en/\nUser will be prompted to select a country and method to chart a graph of.")
		self.__AIDataTTP=CreateToolTip(self.__AIButton, "Google trends data, rating the popularity of the search term 'Artificial Intelligence'\nin the search engine on a scale of 1-100, monthly since 2004. \nSourced from https://trends.google.com/trends/explore?date=all&geo=US&q=%2Fm%2F0mkz")
		self.__UserDataButtonTTP=CreateToolTip(self.__UserDataButton, "Upload your own data. Should be a CSV file with first two comma-delimited\nvalues being x and y axis titles, followd by x and y data in delimited pairs \nseparated by line breaks.")

	def WHOdata(self):
		filepath=os.path.dirname(os.path.realpath(__file__))
		malariapath=(os.path.dirname(filepath)+"/CSV Data Files/malaria_data_cleaned.csv")
		with open(malariapath) as csvdata:
			listOfCountries = []
			self.__malariaDataRaw = []
			for j in csvdata:
				listOfCountries.append((j.split(",")[0]))
				self.__malariaDataRaw.append(j)
		self.__malariaData=[]
		for i in self.__malariaDataRaw:
			self.__malariaData.append(i[:-1])
		#split malaria data into a dictionary with country=key and list of cases for years 2011-2017 as item
		self.__malariaDict={}
		for k in self.__malariaData:
			self.__malariaDict[(k.split(","))[0]]=(k.split(","))[1:len(k)]
		self.__WHOButton.destroy()
		self.__AIButton.destroy()
		self.__UserDataButton.destroy()
		self.__selectedCountry=tkinter.StringVar(self.__dataMenu)
		self.__selectedCountry.set(listOfCountries[0])
		self.__countriesDropdown = tkinter.OptionMenu(self.__dataMenuFrame,self.__selectedCountry,*listOfCountries)
		self.__countriesDropdown["highlightthickness"]=0
		self.__simpleLabel=tkinter.Label(self.__dataMenuFrame,text="Select a country:",bg=self.__coolbluedark)
		self.__infoLabel=tkinter.Message(self.__dataMenuFrame,text="Note: For the Malaria data, the eight years of data is spread across 240 on the x axis for readability, and the population data is squashed to fit onto the scale.",justify="left", bg=self.__coolblue)
		self.__nextbutton=tkinter.Button(self.__dataMenuFrame,text="Select",command=self.WHODataCallback1)
		self.__infoLabel.grid(row=0,column=1)
		self.__simpleLabel.grid(row=1,column=1)
		self.__countriesDropdown.grid(row=2,column=1)
		self.__nextbutton.grid(row=3,column=1)
	def WHODataCallback1(self):
		selectedCountry=self.__selectedCountry.get()
		selectedData=self.__malariaDict[selectedCountry]
		#diknotsayanalysismethods
		self.__countriesDropdown.destroy()
		self.__simpleLabel.destroy()
		self.__nextbutton.destroy()
		self.__infoLabel.destroy()
		#since this malaria data is a little different, we need to create the CSV file that will be sent to the analysis function
		filepath=os.path.dirname(os.path.realpath(__file__))
		csvfolderpath=(os.path.dirname(filepath)+"/CSV Data Files")
		filepath=csvfolderpath+"/temporary.csv"
		with open(filepath,mode="w",newline="") as datafile:
			datafilewriter=csv.writer(datafile,delimiter=",",quotechar='"',quoting=csv.QUOTE_MINIMAL)
			datafilewriter.writerow(["Year","{0}Number of malaria cases scaled to fit range of screen".format(selectedCountry)])
			maximum=0
			for j in self.__malariaDict[selectedCountry]:
				val=int(j)
				if val>maximum:
					maximum=val
			minimum = maximum
			for j in self.__malariaDict[selectedCountry]:
				val=int(j)
				if val<minimum:
					minimum=val
			print("Data range:",minimum,maximum)
			print(self.__w,self.__h)
			for i in range(0,len(self.__malariaDict[selectedCountry])):
				val=int((self.__malariaDict[selectedCountry])[i])
				datafilewriter.writerow([(len(self.__malariaDict[selectedCountry])-(i))*((self.__h/2)+25)/8,int((((self.__w/2)+25)/(maximum-minimum))*(val-minimum))])
		self.__CSVfilePath = filepath
		self.AnalysisMethodSelection()
		


	def AIdata(self):
		self.__WHOButton.destroy()
		self.__AIButton.destroy()
		self.__UserDataButton.destroy()
		filepath=os.path.dirname(os.path.realpath(__file__))
		csvfolderpath=(os.path.dirname(filepath)+"/CSV Data Files")
		filepath=csvfolderpath+"/AIData.csv"
		self.__CSVfilePath=filepath
		self.AnalysisMethodSelection()

	def UserData(self):
		self.__CSVfilePath=tkinter.filedialog.askopenfilename(initialdir = "~/Documents",title = "Select CSV file",filetypes = [("CSV files","*.csv")])
		if self.__CSVfilePath!=():
			self.AnalysisMethodSelection()
	def AnalysisMethodSelection(self):
		methods=["Linear Regression","Polynomial Regression","Exponential Regression","B-splines"]
		self.__methodsDropdown = tkinter.Listbox(self.__dataMenuFrame,bg="light grey",relief=tkinter.FLAT,highlightbackground=self.__coolblue)
		for i in range (len(methods)):
			self.__methodsDropdown.insert(i+1,methods[i])
		self.__chiSquaredVar = tkinter.StringVar()
		self.__chiSquaredVar.set(0)
		self.__chiSquaredCheckbox = tkinter.Checkbutton(self.__dataMenuFrame,bg=self.__coolbluedark,text="Chi-Squared test?",variable=self.__chiSquaredVar)
		nextbutton=tkinter.Button(self.__dataMenuFrame,image=self.__gearIcon,command=self.AnalysisMethodSelection2)
		nextbuttonTTP=CreateToolTip(nextbutton,"Analyse")
		self.__dataMenuFrame.grid_columnconfigure(1,weight=2)
		self.__methodsDropdown.grid(row=3,column=1,sticky="S",pady=10)
		nextbutton.grid(row=4,column=1)
		self.__chiSquaredCheckbox.grid(row=0,column=1)
	def AnalysisMethodSelection2(self):
		print("banana",self.__chiSquaredVar.get(),type(self.__chiSquaredVar.get()),int(self.__chiSquaredVar.get().strip(" ")))
		if self.__chiSquaredVar.get():
			print("hit")
			self.chiSquared()
			print("hit2")
		instance = CreateEquation(self.__CSVfilePath,self.__methodsDropdown.get(self.__methodsDropdown.curselection()))
		equ=instance.getEquations()
		x=-1
		if isinstance(equ,list):
			for i in equ[:(len(equ)-1)]:
				x+=1
				print (equ[len(equ)-1][x:x+2])
				self.dataButtonCallback(None,i,equ[len(equ)-1][x:x+2])
		else:
			self.dataButtonCallback(None,equ,None)

	def chiSquared(self):
		print("performing chi-squared test")
	def userEnterValues(self,h,w):
		self.__equationWindow=tkinter.Toplevel()
		self.__equationWindow.title("Enter an equation")
		self.__equationInfo=tkinter.Label(self.__equationWindow,text="Enter an equation:", anchor="w").grid(columnspan=2,padx=5,pady=5)
		self.__equationEntry = tkinter.Entry(self.__equationWindow)
		self.__equationEntry.focus_set()
		self.__equationEntry.grid(row=1,column=0, padx=5, pady=0, columnspan=2)
		#self.__equationWindow.bind("<Return>", self.defineEquation(None, self.__equationEntry.get()))
		#QOL change, enter sends the entry also instead of clicking button
		self.__equationWindow.bind("<Return>",lambda event:self.equationButtonCallback(None, self.__equationEntry.get()))
		self.__equationEntered = tkinter.Button(self.__equationWindow,text="Enter", command=lambda:self.equationButtonCallback(None, self.__equationEntry.get()))
		self.__equationEntered.grid(row=2,column=1, padx=5, pady=5)
		self.__cancelEquation = tkinter.Button(self.__equationWindow,text="Cancel", command= lambda: self.__equationWindow.destroy())
		self.__cancelEquation.grid(row=2,column=0, padx=5, pady=5)
	def zoom(self,h,w,zin):
		self.__screen.clear()
		self.__canvas.delete(self.__zoomoutwindow,self.__zoominwindow)
		if zin:
			self.__zfactor=self.__zfactor*3/2
			self.__canvas.scale("all",0,0,3/2,3/2)
		else:
			self.__zfactor=self.__zfactor*2/3
			self.__canvas.scale("all",0,0,2/3,2/3)
		self.__zoomoutwindow=self.__canvas.create_window(w-300*(w/500),h-260*(h/500),anchor="sw", height=50, width=50, window=self.__zoomoutButton)
		self.__zoominwindow=self.__canvas.create_window(w-(300*(w/500)+60),h-260*(h/500),anchor="sw", height=50, width=50,window=self.__zoominButton)
		self.drawAxis(w,h)
		self.addLabels((w*self.__zfactor**-1),(h*self.__zfactor**-1),w,h)
	def clearCanvas(self):
		self.__pen2.clear()
		self.__pen2.penup()
		self.__pen2.goto(0,0)
	def buttons(self,h,w,init):
		self.__zfactor=1
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
		self.__mosquitoIcon=ImageTk.PhotoImage(self.__iconlist[5])
		self.__AIICon=ImageTk.PhotoImage(self.__iconlist[6])
		self.__uploadIcon=ImageTk.PhotoImage(self.__iconlist[7])
		self.__gearIcon=ImageTk.PhotoImage(self.__iconlist[8])
		self.__coolblue="#46ACC2"
		self.__coolbluedark="#3b91a3"
		self.__canvasButton = tkinter.Button(self.__root,image=self.__canvasIcon,width=62,height=62,command=self.canvasButtonCallback, highlightthickness=0, bd=0, bg=self.__coolblue, activebackground=self.__coolbluedark)#a button to change the colour of the turtle
		self.__canvasButton.grid(row=0,column=0, sticky="n",pady=0)
		self.__equationButton = tkinter.Button(self.__root,image=self.__equationIcon,command=lambda: self.userEnterValues(h,w), highlightthickness=0, bd=0,width=62,height=62, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__equationButton.grid(row=1,column=0, sticky="n",pady=0)
		self.__manualButton=tkinter.Button(self.__root,image=self.__manualIcon,command=self.manual, highlightthickness=0, bd=0,width=62,height=62, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__manualButton.grid(row=124, sticky="s",pady=0)
		self.__dataButton = tkinter.Button(self.__root,image=self.__tableIcon,command=self.dataMenu, highlightthickness=0, bd=0,width=62,height=62, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__dataButton.grid(row=2,column=0, sticky="n",pady=0)
		self.__clearButton = tkinter.Button(self.__root,image=self.__clearIcon,command=self.clearCanvas, highlightthickness=0, bd=0,width=62,height=62, bg=self.__coolblue, activebackground=self.__coolbluedark)
		self.__clearButton.grid(row=3, sticky="n",pady=0)
		zoomfont = tkinter.font.Font(family='Helvetica', size=26, weight="bold")
		self.__zoominButton=tkinter.Button(self.__root, text="+", command=lambda: self.zoom(h,w,True),highlightthickness=0, bd=0,font=zoomfont,height=1,width=1)
		self.__zoominwindow=self.__canvas.create_window(w-(300*(w/500)+60),h-260*(h/500),anchor="sw",height=50, width=50, window=self.__zoominButton)
		self.__zoomoutButton=tkinter.Button(self.__root, text="-", command=lambda: self.zoom(h,w,False),highlightthickness=0, bd=0,font=zoomfont,height=1,width=1)
		self.__zoomoutwindow=self.__canvas.create_window(w-300*(w/500),h-260*(h/500),anchor="sw",height=50, width=50, window=self.__zoomoutButton)
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
				column=column+1#column is increase
	def doResize(self):
		self.__resizeConfirm.destroy()
		self.__canvas.grid_forget()
		self.__sideBarCanvas.grid_forget()
		self.setupScreen(int(self.__resizeXEntry.get()),int(self.__resizeYEntry.get()),False)
		self.__canvasWindow.destroy()
	def resizeWarning(self):
		x=Image.open(os.path.dirname(os.path.realpath(__file__))+"/Icons/warning.png")
		self.__warningIcon=ImageTk.PhotoImage(x)
		self.__resizeConfirm=tkinter.Toplevel(self.__root)
		self.__resizeConfirm.title("Warning")
		self.__warning=tkinter.Label(self.__resizeConfirm, image=self.__warningIcon).grid(row=0,column=0, padx=3, pady=3)
		self.__cropButton=tkinter.Button(self.__resizeConfirm,text="Confirm",command=self.doResize)
		self.__cancelButton2=tkinter.Button(self.__resizeConfirm,text="Cancel",command=lambda: self.__resizeConfirm.destroy())
		self.__cropLabel=tkinter.Label(self.__resizeConfirm, text="Warning! Resizing will clear your canvas. Continue?").grid(row=0, column=1, columnspan=2, padx=3, pady=3)
		self.__cropButton.grid(row=1, column=2, padx=3, pady=3)
		self.__cancelButton2.grid(row=1, column=1, padx=3, pady=3)
		self.__resizeConfirm.grid()
	def canvasButtonCallback(self): #a subroutine for changing the colour of the pen
		self.__canvasWindow=tkinter.Toplevel(self.__root)
		self.__canvasWindow.title("Canvas")
		self.__colorLabel=tkinter.Label(self.__canvasWindow, text="Colour:").grid(row=0, column=0, padx=5, pady=10,sticky="w")
		self.__colorButton=tkinter.Button(self.__canvasWindow,highlightthickness=0,background=self.__pen2.color()[0], activebackground=self.__pen2.color()[0], command=self.colourWindow)
		self.__colorButton.grid(row=0, column=1, padx=2, pady=(0,5),sticky="w")
		self.__resizeButton=tkinter.Button(self.__canvasWindow, text="Resize",command=self.resizeWarning)
		self.__resizeButton.grid(row=3,column=1,padx=2, pady=(5,0))
		self.__resizeXlabel=tkinter.Label(self.__canvasWindow,text="Width:").grid(row=1,column=0,padx=2,pady=2, sticky="w")
		self.__resizeYlabel=tkinter.Label(self.__canvasWindow,text="Height:").grid(row=2,column=0,padx=2,pady=2, sticky="w")
		self.__resizeXEntry=tkinter.Entry(self.__canvasWindow, width=4)
		self.__resizeXEntry.insert(0,str(self.__canvas.winfo_width()-2))
		self.__resizeXEntry.grid(row=1,column=1,padx=2,pady=2,sticky="w")
		self.__resizeYEntry=tkinter.Entry(self.__canvasWindow,width=4)
		self.__resizeYEntry.insert(0,str(self.__canvas.winfo_height()-2))
		self.__resizeYEntry.grid(row=2,column=1,padx=2,pady=2,sticky="w")
		self.__cancelButton=tkinter.Button(self.__canvasWindow, text="Close", command=lambda: self.__canvasWindow.destroy())
		self.__cancelButton.grid(row=3, column=0, padx=2, pady=(5,0))
		self.__canvasWindow.grid()
	def colour(self,colour):
		self.__pen2.pencolor(colour)
		self.__colourinwindow.destroy()
		self.__canvasWindow.destroy()
		self.canvasButtonCallback()
	def dataButtonCallback(self,event,equ,knots):
		self.__dataMenu.destroy()
		self.defineEquation(equ,knots)
	def equationButtonCallback(self,event,equ):
		self.__equationWindow.destroy()
		self.defineEquation(equ,None)
	def defineEquation(self,equ,knots):
		h,w=self.__h,self.__w
		self.__equation=equ
		self.__equation=self.__equation.replace(" ","")
		eqlist=[char for char in self.__equation]
		for i in range(len(eqlist)): #put exponentials in the right form
		    if eqlist[i]=="e" and eqlist[i+1]=="^":
		        for j in range (len(eqlist[(i+2):])):
		            if eqlist[(i+2):][j].isdigit()==False and eqlist[(i+2):][j]!="x" and eqlist[(i+2):][j]!="/" and eqlist[(i+2):][j]!="-" and eqlist[(i+2):][j]!=".":
		                eqlist.insert((i+2+j),")")
		                break
		            elif (j+1)==len(eqlist[(i+2):]):
		                eqlist.append(")")
		        self.__equation="".join(eqlist)
		        self.__equation=self.__equation.replace("e^"," math.exp(")
		self.__equation=self.__equation.replace("^","**") #Put powers in the right form
		self.__equation=self.__equation.replace(" ","")
		eqlist=[char for char in self.__equation]
		for i in range(len(eqlist)): #Put multiplication in the right form
		    if eqlist[i]=="x" and i!=0 and (eqlist[i-1].isdigit()or eqlist[i-1]==")") or (eqlist[i]=="m" and i!=0 and (eqlist[i-1].isdigit()or eqlist[i-1]==")"or eqlist[i-1]=="x")):
			    eqlist.insert(i, "*")
		self.__equation="".join(eqlist)
		self.equationBounds(h,w,knots)
	def equationBounds(self,h,w,knots):
		print (self.__equation)
		x=sympy.Symbol("x")
		if "exp" in self.__equation:
			boundlist=[]
			try:
			    boundlist.append([sympy.nsolve(eval(self.__equation.replace("math.exp","sympy.exp"))-((self.__zfactor**(-1))*(h/2+25)),(-h/2,h/2),solver="bisect")])
			except:
			    pass
			try:
			    boundlist.append([sympy.nsolve(eval(self.__equation.replace("math.exp","sympy.exp"))+((self.__zfactor**(-1))*(h/2+25)),(-h/2,h/2),solver="bisect")])
			except:
			    pass
		else:
			print ([sympy.solvers.solve(eval(self.__equation.replace("math.exp","sympy.exp"))-((self.__zfactor**(-1))*(h/2+25)),x),sympy.solvers.solve(eval(self.__equation.replace("math.exp","sympy.exp"))+((self.__zfactor**(-1))*(h/2+25)),x)])
			boundlist=[sympy.solvers.solve(eval(self.__equation.replace("math.exp","sympy.exp"))-((self.__zfactor**(-1))*(h/2+25)),x),sympy.solvers.solve(eval(self.__equation.replace("math.exp","sympy.exp"))+((self.__zfactor**(-1))*(h/2+25)),x)]
		for i in range(len(boundlist)):
			newlist=[]
			for j in range(len(boundlist[i])):
				if "I" not in str(boundlist[i][j]):
					newlist.append(eval(str(boundlist[i][j]).replace("sqrt","math.sqrt").replace("log","math.log")))
			boundlist[i]=newlist
		boundlist = [item for sublist in boundlist for item in sublist]
		for i in boundlist:
			if i==[]:
				boundlist.remove(i)
		boundlist=sorted(boundlist)
		self.drawGraph(boundlist,w,knots)
	def drawGraph(self,boundlist,w,knots):
		self.__observed=[]
		self.__pen2.penup()
		self.__pen2.speed(0)
		if knots==None:
			self.__pen2.goto(0,0)
		else:
			x1=knots[0]
		if "exp" not in self.__equation and knots==None:
			x1=boundlist[0]
		elif "exp" in self.__equation:
			pass
			if "-" in self.__equation.split(".exp(",1)[1]:
				x1=boundlist[0]
				boundlist.append(w*self.__zfactor**(-1)/2)
			else:
				x1=-(w*self.__zfactor**(-1)/2)
		if knots!=None:
			x2=knots[1]
		else:
			print (boundlist)
			x2=boundlist[len(boundlist)-1]
		while x1<=x2:
			y=eval(self.__equation.replace("x","("+str(x1)+")").replace("e"+"("+str(x1)+")"+"p","exp").replace("sympy","math"))
			self.__pen2.goto(self.__zfactor*x1,self.__zfactor*y)
			self.__pen2.pendown()
			if knots==None:
				self.__observed.append([x1,y])
			x1=x1+1
		y=eval(self.__equation.replace("x","("+str(x2)+")").replace("e"+"("+str(x2)+")"+"p","exp").replace("sympy","math"))
		self.__pen2.goto(self.__zfactor*x2,self.__zfactor*y)
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
class CreateEquation():
	def __init__(self,datafilepath,selectedmethod):
		self.__method=selectedmethod
		equations=[]
		path1=os.path.dirname(os.path.realpath(__file__))
		self.__knots=""
		if self.__method=="Exponential Regression":
			csvin=os.path.basename(datafilepath)
			path1=os.path.dirname(datafilepath)+"/"
			cmd=["Rscript",os.path.dirname(os.path.dirname(path1))+"/Regression Programs/exponential_R.r",str(csvin),path1]
			x=subprocess.check_output(cmd, universal_newlines=True)
			a=((re.split("\n",x)[4]).strip()).split(" ",2)[0]
			b=((re.split("\n",x)[4]).strip()).split(" ",2)[1]
			self.__equations=str(a+"e^"+b+"x")
		if self.__method=="Polynomial Regression":
			csvin=os.path.basename(datafilepath)
			path1=os.path.dirname(datafilepath)+"/"
			cmd=["Rscript",os.path.dirname(os.path.dirname(path1))+"/Regression Programs/quadratic_R.r",str(csvin),path1] #makes a command to launch the r program, passes the user's path and the input
			#lil batch script run from python
			x=subprocess.check_output(cmd, universal_newlines=True) #Sets x to the output of the command
			#which is the output of the final line of rtesting.r (the linear regression coefficients). universal_newlines forces it to work with linux and windows line endings
			interceptandxcoefficient=re.split("\n",x)[1]
			xsquaredcoefficient=float((re.split("\n",x)[3]).strip())
			inteceptandxcoefficientsplit = re.split(" ",interceptandxcoefficient)
			foo=0
			for value in inteceptandxcoefficientsplit:
			    if len(value)>1:
			        if foo==0:
			            intercept=float(value)
			            foo+=1
			        else:
			            xcoefficient=float(value)
			self.__equations="".join([str(xsquaredcoefficient),"x^2+",str(xcoefficient),"x+",str(intercept)])
		if self.__method=="Linear Regression":
			csvin=os.path.basename(datafilepath)
			path1=os.path.dirname(datafilepath)+"/"
			cmd=["Rscript",os.path.dirname(os.path.dirname(path1))+"/Regression Programs/linear_R.r",str(csvin),path1] #makes a command to launch the r program, passes the user's path and the input
			#lil batch script run from python
			x=subprocess.check_output(cmd, universal_newlines=True) #Sets x to the output of the command
			#which is the output of the final line of rtesting.r (the linear regression coefficients). universal_newlines forces it to work with linux and windows line endings
			print(x)
			intercept=((re.split("\n",x)[1]).strip()) #Isolates the numbers from the output
			grad=((re.split("\n",x)[3]).strip())#And stores them in their related variables 
			self.__equations=str(grad)+"x+"+str(intercept)
		if self.__method=="B-splines":
			csvin=os.path.basename(datafilepath)
			path1=os.path.dirname(datafilepath)+"/"
			cmd=["Rscript",os.path.dirname(os.path.dirname(path1))+"/Regression Programs/splines_R.r",str(csvin),path1] #makes a command to launch the r program, passes the user's path and the input
			#lil batch script run from python
			x=subprocess.check_output(cmd, universal_newlines=True) #Sets x to the output of the command
			coeffs=[k for k in [each[1:] for each in ([j for j in [re.split(" ",i) for i in (re.split("\n",x)[9:13])] if j!=" "])]]
			for z in range(len(coeffs)):
				templist=[]
				for i in range (len(coeffs[z])):
					if len(coeffs[z][i])!=0:
						templist.append(coeffs[z][i])
				coeffs[z]=templist
			self.__equations=[]
			for i in range (0,5):
				self.__equations.append(coeffs[3][i]+"x^3+"+coeffs[2][i]+"x^2+"+coeffs[1][i]+"x+"+coeffs[0][i])
			self.__equations.append([eval(z) for z in [j for k in [re.split(" ",i) for i in re.split("  ",(re.split("\n",x))[15])[1:]] for j in k] if z!=""])
	def getEquations(self):
		return self.__equations

instance = Application(tkinter.Tk())