# Team: Charles Pratt
#
# 317 Regression Project: Governace


# Clean up the environment.
rm(list=ls())

require(ggplot2)
require(GGally)
require(VGAM)



# data  <- read.csv("317-SP-comps.csv", stringsAsFactors=FALSE)
data  <- read.csv("317-MCapUS-comps.csv", stringsAsFactors=FALSE)
attach(data)

# Create Output File
write("", file = "Reults.txt", append = FALSE)
if (!dir.exists("img")) {
  dir.create("img")
}

dependents  <- list("Board_Size", "AVG_Tenure", "AVG_Seats", "AVG_Prime", "Score")
for (d in dependents) {
  write("#################################", file = "Reults.txt", append = TRUE)
  write(d, file = "Reults.txt", append = TRUE)
  write("#################################", file = "Reults.txt", append = TRUE)

  depen <- eval(as.name(d))
  reg <- lm(depen ~ Market_Cap + State + Op_Rev + Num_Employees + Sector +
               CAGR5 + M_OWNED + W_OWNED + Num_Employees + Assets + Total_Cash +
               Profit_Margin + Num_Share + Num_Subs)
  s <- summary(reg)
  capture.output(s, file = "Reults.txt", append = TRUE)
  write("\n\n", file = "Reults.txt", append = TRUE)

  file_name <- paste("img/", d, "_residual.png", sep = "")
  png(file_name)
  reg.res = resid(reg)
  title <- paste(d,": Residual plot")
  plot(data$CAGR5, reg.res, main=title,
       xlab="CAGR",
       ylab="Residuals", col="blue")
  abline(a=0,b=0)
  dev.off()
}

# Plot just CAGR
regCAGR <- lm(Score ~ CAGR5)
summary(regCAGR)
file_name <- paste("img/", "CAGR Only", ".png", sep = "")
png(file_name)

# e_reg <- lm(price ~ temp)
plot(CAGR5, Score, main="Mid Cap",
     xlab="5 year CAGR",
     ylab="Board Score", col="blue")
abline(regCAGR, col="red", lwd=3)
dev.off()

detach(data)
