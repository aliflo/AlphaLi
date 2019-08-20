#space for testing stuff in r
pyin <- commandArgs(trailingOnly=TRUE) #gets the arguments that python passed in
setwd(pyin[2]) #Sets the directory to the one passed in from the python program
csvfile <- read.csv(file=pyin[1]) #Reads the csv file as listed by python
formula1 <- as.formula(paste(as.name(colnames(csvfile)[1])," ~ ",as.name(colnames(csvfile)[2]))) #Makes the formula for linear regression on the csv file
lm(formula1, data=csvfile)$coefficients #Returns the regression of that formula ($coefficients makes it so only the relevant bits are passed in)