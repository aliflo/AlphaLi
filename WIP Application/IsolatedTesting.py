import os
path=os.path.dirname(os.path.realpath(__file__))
print(path)
path2=path+"\Icons"
print(os.listdir(path2))




##from tkinter import *
##root=Tk()
##elist=[]
##def up(event):
##	print (elist.index(event.widget))
##	if elist.index(event.widget)!=0:
##		elist[elist.index(event.widget)-1].focus_set()
##def down(event):
##	print (elist.index(event.widget))
##	if elist.index(event.widget)!=3:
##		elist[elist.index(event.widget)+1].focus_set()
##for i in range(4):
##	e=Entry(root)
##	e.grid(row=i)
##	e.bind("<Up>",up)
##	e.bind("<Down>",down)
##	elist.append(e)
