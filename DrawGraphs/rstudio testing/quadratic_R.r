#see comments linear_R
pyin <- commandArgs(trailingOnly=TRUE)#c("AIData.csv","C:/Users/tom/OneDrive/Documents/SWCHS/A-Levels/EPQ/DrawGraphs/DrawGraphs/rstudio testing")
#
setwd(pyin[2])
csvfile <- read.csv(file=pyin[1],header=TRUE)
names(csvfile) <- c("months","searchInterest")
lm(csvfile$searchInterest ~ poly(csvfile$months, 2, raw=TRUE))$coefficients