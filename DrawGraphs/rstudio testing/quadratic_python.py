#see commenting for linear_python.py
import subprocess
import os
import re
path1=os.path.dirname(os.path.realpath(__file__))
print(path1)
csvin=input("Give a csv file: ")
cmd=["Rscript","quadratic_R.r",str(csvin),path1]
x=subprocess.check_output(cmd,universal_newlines=True)

intercept=float((re.split("\n",x)[1]).strip())
xsquaredcoefficient=float((re.split("\n",x)[5]).strip())
xcoefficient=float((re.split("\n",x)[3]).strip())
