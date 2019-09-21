import colorsys
import math
with open("rgb.txt") as f:
    biglist=f.readlines()
biglist=[x.strip() for x in biglist]
biglist=[x.split("		") for x in biglist]
for i in range(0,len(biglist)):
    #biglist[i][0]=[int(b) for b in [[a.split(" ") for a in biglist[i][0]]]]
    if len(biglist[i][0].split(" "))>3:
        a=[]
        for j in biglist[i][0].split(" "):
            if j!=" " and j!="":
                a.append(str(j))
                a.append(" ")
        biglist[i][0]="".join(a[:5])
    biglist[i][0]=[int(b) for b in biglist[i][0].split(" ")]
colours=[]
names=[]
for i in range(0,len(biglist)):
    colours.append(biglist[i][0])
    names.append(biglist[i][1])

def step (r,g,b,repetitions):
	lum=math.sqrt(0.241*r+0.691*g+0.068*b)
	h,s,v=colorsys.rgb_to_hsv(r,g,b)
	h2 = int(h * repetitions)
	lum2 = int(lum * repetitions)
	v2 = int(v * repetitions)
	return (h2, lum, v2)
zipped=zip(colours,names)
colours, names=zip(*sorted(zipped,key=lambda rgb: step(*(rgb[0]),8)))
print (names)

