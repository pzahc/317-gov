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
reg1 <- lm(AVG_Tenure ~ AVG_Seats + Market_Cap + State + Op_Rev + Num_Employees + Sector)
summary(reg1)

reg2 <- lm(AVG_Seats ~ AVG_Tenure + Market_Cap + State + Op_Rev + Num_Employees + Sector)
summary(reg2)

reg3 <- lm(CP_Score ~ Market_Cap + State + Op_Rev + Num_Employees + Sector)
summary(reg3)

detach(data)
