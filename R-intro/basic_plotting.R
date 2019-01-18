#plotting made easy with R once you get familiar with syntax
data <- read.table("AirPassengers.txt", header = TRUE)
summary(data)
hist(data$AGE)
hist(data$HEIGHT)
#we can also plot two values against each other to see their relation
plot(data$WEIGHT, data$CHOL)
plot(data$AGE, data$CHOL)

#boxplots in R

boxplot(CHOL ~ SMOKE, data = data, col = "lightgray")