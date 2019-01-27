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


#using the mtcars data set
#clean/normalize the data
data(mtcars)
mydata = na.omit(mtcars) #deletion of missing
mydata = scale(mydata) #standarize variables

# Determine number of clusters
wss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))
for (i in 2:15) wss[i] <- sum(kmeans(mydata, 
                                     centers=i)$withinss)
plot(1:15, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares")
# check out the plot


# K-Means Cluster Analysis
fit <- kmeans(mydata, 5) # 5 cluster solution
# get cluster means 
aggregate(mydata,by=list(fit$cluster),FUN=mean)
# append cluster assignment
mydata <- data.frame(mydata, fit$cluster)

#visualize the clustering results
library(cluster) 
clusplot(mydata, fit$cluster, color=TRUE, shade=TRUE, labels=2, lines=0)