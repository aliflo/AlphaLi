pyin <- commandArgs(trailingOnly=TRUE) #Gets inputs from python and stores them
setwd(pyin[2]) #Sets the working directory to be the one recieved from python
csvfile <- read.csv(file=pyin[1]) #Reads the csv that python instructed
col1<-unlist(lapply(csvfile[colnames(csvfile)[1]], log))
col2<-unlist(lapply(csvfile[colnames(csvfile)[2]], log)) #Takes logs of all the items in the first two columns and stores them in new columns
a_start<-as.numeric(summary(lm(col2~col1))$coefficients[2])
b_start<-as.numeric(summary(lm(col2~col1))$coefficients[4]) #Creates the start points from linear regression coefficients of the logs
newMod <- nls(col1 ~ a*col2^b, data=csvfile, start = list(a=exp(a_start),b=exp(b_start)))
f=as.formula(paste(as.name(colnames(csvfile)[2]),"~I(a*exp(b*",as.name(colnames(csvfile[1])),"))")) #Makes a formula that does exponential regression on the data
expo<-nls(newMod,data=csvfile, start=list(a=exp(a_start),b=b_start)) #Does the exponential regression and stores the results
expo #Outputs the results