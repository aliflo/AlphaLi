#see comments linear_R
pyin <- commandArgs(trailingOnly=True)
setwd(pyin[2])
csvfile <- read.csv(file=pyin[1],header=TRUE)
names(csvfile) <- c("months","searchInterest")
lm(csvfile$searchInterest ~ poly(csvfile$months, 2, raw=TRUE))$coefficients