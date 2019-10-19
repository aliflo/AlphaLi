import os

filepath=os.path.dirname(os.path.realpath(__file__))
malariapath=(os.path.dirname(filepath)+"\\CSV Data Files\\AIData.csv")

print(os.path.dirname(malariapath))
print(os.path.basename(malariapath))
