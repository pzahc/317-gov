# Team: Charles Pratt
#
# 317 Regression Project: Governace


# Clean up the environment.
rm(list=ls())

require(ggplot2)
require(GGally)
require(VGAM)



data  <- read.csv("317-tech-ready.csv", stringsAsFactors=FALSE)
attach(data)
reg1 <- lm(Score ~ Company)
summary(reg1)

detach(data)
