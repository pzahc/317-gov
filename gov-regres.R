# Team: Charles Pratt
#
# 317 Regression Project: Governace


# Clean up the environment.
rm(list=ls())

require(ggplot2)
require(GGally)
require(VGAM)



data  <- read.csv("317-tech-comps.csv", stringsAsFactors=FALSE)
attach(data)
reg1 <- lm(Market_Cap ~ State + Op_Rev + Num_Employees)
summary(reg1)

detach(data)
