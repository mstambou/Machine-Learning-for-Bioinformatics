#There are different clustering algorithms, these are characterized as non-supervised learning
#let's create a dataset for clustering first

means <- sample(c(-3, 0, 3), 99, replace=TRUE)
x <- rnorm(99, mean=means) #generate a normal random number with mean and standard deviation as specifiec
#to check if we simulated the data correctly, call
#tapply(x, factor(means), mean)

d <- dist(x)
hc <- hclust(d)

#plot the clustering result
plot(hc)
rect.hclust(hc, k=3, border="red")

#check identified clusters
clust <- cutree(hc, k=3)
plot(x ~ factor(means), main="Original Clusters", xlab="Cluster Mean")
plot(x ~ factor(clust), main="Identified Clusters", xlab="Cluster Number")

data(mtcars)
d <- dist(mtcars, method = "euclidean") # distance matrix
fit <- hclust(d, method="ward.D") 
plot(fit, main="hierarchical clustering for mtcars dataset") # display dendogram
groups <- cutree(fit, k=5) # cut tree into 5 clusters
# draw dendogram with red borders around the 5 clusters 
rect.hclust(fit, k=5, border="red")

#using small breas cancer dataset
data0=read.csv("http://homes.sice.indiana.edu/yye/lab/teaching/topics/R/data/cancer-sm.csv")
#strip off the class column
data <- data0[ -c(10) ]
d <- dist(data, method = "euclidean") # distance matrix
fit <- hclust(d, method="ward.D") 
plot(fit, main="hierarchical clustering for cancer dataset") # display dendogram