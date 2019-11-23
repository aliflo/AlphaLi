#knots <- quantile(csvfile$searchInterest, p=c(0.25,0.75))#this line defines two points in the data that are the lower quartile
#and upper quartile. In my data set they come out at 25 and 43. These will be the knots
#install.packages("SplinesUtils")
#ignore this, it's for when it's integrated with python#commandArgs(trailingOnly=TRUE)

library(SplinesUtils)
pyin <- commandArgs(trailingOnly=TRUE)
setwd(pyin[2])#sets working directory to the above string
csvfile <- read.csv(file=pyin[1],header=TRUE)#read.csv(file=pyin[1],header=TRUE)#reads the csv file into a dataframe with headers
names(csvfile) <- c("months","searchInterest")#renames the headers becuase they're very long and cause formatting issues
model <- lm(csvfile$searchInterest ~ bs(csvfile$months, df=7))#a linear model of months against a bspline of search interest
piecewisePoly <- RegBsplineAsPiecePoly(model, "bs(csvfile$months, df = 7)",shift=FALSE)#creates the piecewise polynomials
piecewisePoly
finalcoef <- piecewisePoly$PiecePoly$coef
finalcoef[1, ] <- finalcoef[1, ] + model$coefficients[1]
finalcoef
attr(bs(csvfile$months, df=7),"knots") 
