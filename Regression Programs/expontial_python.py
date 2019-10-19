#exponential python
import subprocess
import os
path1=os.path.dirname(os.path.realpath(__file__))
csvin=input("Give a csv file: ")
cmd=["Rscript","exponential_R.r",str(csvin),path1]
x=subprocess.check_output(cmd, universal_newlines=True)
print (x)