#knots <- quantile(csvfile$searchInterest, p=c(0.25,0.75))#this line defines two points in the data that are the lower quartile
#and upper quartile. In my data set they come out at 25 and 43. These will be the knots
#install.packages("SplinesUtils")
#ignore this, it's for when it's integrated with python#commandArgs(trailingOnly=TRUE)

library(SplinesUtils)
pyin <- c("AIData.csv","C:/Users/tom/OneDrive/Documents/SWCHS/A-Levels/EPQ/DrawGraphs/DrawGraphs/rstudio testing")
setwd <- pyin[2]#sets working directory to the above string
csvfile <- read.csv(file=pyin[1],header=TRUE)#reads the csv file into a dataframe with headers
names(csvfile) <- c("months","searchInterest")#renames the headers becuase they're very long and cause formatting issues
model <- lm(csvfile$searchInterest ~ bs(csvfile$months, df=5))#a linear model of months against a bspline of search interest
piecewisePoly <- RegBsplineAsPiecePoly(model, "bs(csvfile$months, df = 5)",shift=FALSE)#creates the piecewise polynomials
piecewisePoly
piecewisePoly$PiecePoly$coef