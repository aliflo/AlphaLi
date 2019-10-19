import subprocess
import os
import re
path1=os.path.dirname(os.path.realpath(__file__))
print(path1)
csvin="C:/Users/tom/OneDrive/Documents/SWCHS/A-Levels/EPQ/AlphaLi/WIP Application/MainProgram.py"
cmd=["Rscript","splines_R.r",str(csvin),path1]
x=subprocess.check_output(cmd,universal_newlines=True)
print(x)