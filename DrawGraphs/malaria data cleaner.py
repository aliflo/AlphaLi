import csv
import re
with open("malaria_data.csv","r") as csvfile:
    reader=csv.reader(csvfile)
    listofrows=[]
    for row in reader:
        listofrows.append(row)
print(listofrows[2])
for row in range(0,len(listofrows)):
    for item in range(0,len(listofrows[row])):
        if "[" in listofrows[row][item]:
            listofrows[row][item]=re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", listofrows[row][item])
            listofrows[row][item]=listofrows[row][item][:-2]
        listofrows[row][item]=listofrows[row][item].replace(" ","")
for row in listofrows:
    print(row)
with open("malaria_data_cleaned.csv","w") as writefile:
    writer=csv.writer(writefile)
    writer.writerows(listofrows)


            
