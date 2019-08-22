#see commenting for linear_python.py
import subprocess
import os
import re
path1=os.path.dirname(os.path.realpath(__file__))
print(path1)
csvin=input("Give a csv file: ")
cmd=["Rscript","quadratic_R.r",str(csvin),path1]
x=subprocess.check_output(cmd,universal_newlines=True)

"""
Explanation for the code ahead.
In linear regression, there are only two coefficients sent back and they each appear on a single
line: this means you simply select lines 2 and 4 (1 and 3 bbecause python indexing is at 0)
and strip whitespace and convert to a float. However, with polynomial coefficients there are
three coefficients but they don't come on three seperate lines, rather; the intercept and
x coefficient are on line 2 and the x^2 coefficient is on line 4. The below code functions to
first split the variables, one directly into xsquared coefficient as with linear_python.py while
the other is a string with both values in. The string is then split into a list that looks like this:
[' ', ' ', ' ', ' ', ' ', ' ', 'number', ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ', ' ', ' ', 'number', ' ', ' ', ' ', ' ']
the next for loop just takes the two numbers out, the first of which will be the intercept and
the second the xcoefficient. 
"""
print(x)
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
#print(intercept,xcoefficient,xsquaredcoefficient)

#intercept=float((re.split("\n",x)[1]).strip())
#xsquaredcoefficient=float((re.split("\n",x)[5]).strip())
#xcoefficient=float((re.split("\n",x)[3]).strip())
