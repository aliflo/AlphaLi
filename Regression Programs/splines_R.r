#knots <- quantile(csvfile$searchInterest, p=c(0.25,0.75))#this line defines two points in the data that are the lower quartile
#and upper quartile. In my data set they come out at 25 and 43. These will be the knots
#install.packages("SplinesUtils")
#ignore this, it's for when it's integrated with python#commandArgs(trailingOnly=TRUE)

library(SplinesUtils)
pyin <- commandArgs(trailingOnly=TRUE)
csvfile <- read.csv(file=pyin[1])#sets working directory to the above string
col1<-unlist(lapply(csvfile[colnames(csvfile)[1]], log))
col2<-unlist(lapply(csvfile[colnames(csvfile)[2]], log)) #Takes logs of all the items in the first two columns and stores them in new columns
names(csvfile) <- c(col1,col2)#renames the headers becuase they're very long and cause formatting issues
model <- lm(csvfile$searchInterest ~ bs(csvfile$col1, df=7))#a linear model of months against a bspline of search interest
piecewisePoly <- RegBsplineAsPiecePoly(model, "bs(col1$col2, df = 7)",shift=FALSE)#creates the piecewise polynomials
piecewisePoly
finalcoef <- piecewisePoly$PiecePoly$coef
finalcoef[1, ] <- finalcoef[1, ] + model$coefficients[1]
finalcoef
attr(bs(csvfile$col1, df=7),"knots")