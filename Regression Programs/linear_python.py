#python integration testing
#does linear regression on the user's CSV file using R and passes the results back to python
#python passes in the CSV file and gets a result back from R
import subprocess
import os
import re
os.chdir(os.path.dirname(os.path.realpath(__file__)))
bigpath=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/CSV Data Files/"+"AIData.csv" #Gets the path for the current program
csvin=os.path.basename(bigpath)
path1=os.path.dirname(bigpath)+"/"
cmd=["Rscript","linear_R.r",str(csvin),path1] #makes a command to launch the r program, passes the user's path and the input
#lil batch script run from python
x=subprocess.check_output(cmd, universal_newlines=True) #Sets x to the output of the command
#which is the output of the final line of rtesting.r (the linear regression coefficients). universal_newlines forces it to work with linux and windows line endings
intercept=float((re.split("\n",x)[1]).strip()) #Isolates the numbers from the output
grad=float((re.split("\n",x)[3]).strip())#And stores them in their related variables
print (intercept, grad)
