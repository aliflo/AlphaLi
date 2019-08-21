setwd("~/Documents/EPQ/GitPath/DrawGraphs/rstudio testing")
csvfile<-read.csv(file="testdata.csv",header=TRUE
expo<-nls(y~I(a*exp(b*x)),data=csvfile, start=list(a=1,b=1))
#Fits y and x to the model of y=ae^bx