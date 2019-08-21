#space for testing stuff in r
pyin <- commandArgs(trailingOnly=TRUE) #gets the arguments that python passed in
setwd(pyin[2]) #Sets the working directory (setwd) to the one passed in from the python program. pyin[2] is the second value from pyin; not the third - indexing starts at 1 :(
csvfile <- read.csv(file=pyin[1]) #Reads the csv file as listed by python
formula1 <- as.formula(paste(as.name(colnames(csvfile)[1])," ~ ",as.name(colnames(csvfile)[2]))) #Makes the formula for linear regression on the csv file
#variable formula1 defined as.formula: forces what's inside to be recognized as a formula data type. 
#paste (concatenates into text? only half understand) as a 
#name (as.name) column names (colnames) as the first column name of the csv file 
#Tilde means "do regresssion on these two columns" in R formula notation 
#second column is the column name of the second column
lm(formula1, data=csvfile)$coefficients 
#Returns the regression of that formula ($coefficients makes it so only the relevant bits are passed in, i.e. the coefficients of x and c)
#in the python program they are referred to as "gradient" and "intercept"