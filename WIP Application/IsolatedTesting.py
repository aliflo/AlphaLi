import math,sympy

string="x^2"
slist=[char for char in string]
for i in range(len(slist)): #put exponentials in the right form
    if slist[i]=="e" and slist[i+1]=="^":
        for j in range (len(slist[(i+2):])):
            if slist[(i+2):][j].isdigit()==False:
                slist.insert((i+2+j),")")
                break
            elif (j+1)==len(slist[(i+2):]):
                slist.append(")")
        string="".join(slist)
        string=string.replace("e^"," math.exp(")
string=string.replace("^","**") #Put powers in the right form
slist=[char for char in string]
for i in range(len(slist)): #Put multiplication in the right form
    if slist[i]=="x" and i!=0 and slist[i-1].isdigit():
        slist.insert(i, "*")
string="".join(slist)
print (string)
x=sympy.Symbol("x")
print (sympy.solvers.solve(eval(string)-250,x)[0])

