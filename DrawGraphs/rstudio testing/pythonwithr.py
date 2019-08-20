#python integration testing
import subprocess
import os
import re
path1=os.path.dirname(os.path.realpath(__file__)) #Gets the path for the current program
csvin=input("Give a csv file: ")
cmd=["Rscript","rtesting.r",str(csvin),path1] #makes a command to launch the r program, passes the user's path and the input
x=subprocess.check_output(cmd, universal_newlines=True) #Sets x to the output of the command
intercept=float((re.split("\n",x)[1]).strip()) #Isolates the numbers from the output
grad=float((re.split("\n",x)[3]).strip())#And stores them in their relative variables

