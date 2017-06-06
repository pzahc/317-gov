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

# Create Output File
write("", file = "Reults.txt", append = FALSE)
dependents  <- list("AVG_Tenure", "AVG_Size", "Score")

for (d in dependents) {
  write("\n\n#################################   ", file = "Reults.txt", append = TRUE)
  write(d, file = "Reults.txt", append = TRUE)
  write("#################################", file = "Reults.txt", append = TRUE)

  depen <- eval(as.name(d))
  reg <- lm(depen ~ Market_Cap + State + Op_Rev + Num_Employees + Sector +
               CARG5 + M_OWNED + W_OWNED + Num_Employees + Assets + Total_Cash +
               Profit_Margin)
  s <- summary(reg)
  capture.output(s, file = "Reults.txt", append = TRUE)

  # file_name <- paste("img/", t, "_residual.png", sep = "")
  # png(file_name)
  # t_reg.res = resid(t_reg)
  # title <- paste(t,": Win Streak Residual plot")
  # plot(team_subset$WinStreak, t_reg.res, main=title,
  #      xlab="WinStreak",
  #      ylab="Residuals", col="blue")
  # abline(a=0,b=0)
  # dev.off()
}


detach(data)
