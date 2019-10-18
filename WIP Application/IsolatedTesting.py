import os
filepath=os.path.dirname(os.path.realpath(__file__))
malariapath=(os.path.dirname(filepath)+"\\CSV Data Files\\malaria_data_cleaned.csv")
with open(malariapath) as data:
    k=[]
    for j in data:
        k.append(j)
    data=[]
    for l in k:
        p=l[:-1]
        data.append(p)

        
    print(data)
    print(k)