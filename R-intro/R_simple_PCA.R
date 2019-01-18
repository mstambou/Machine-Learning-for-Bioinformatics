mtcars.pca <- prcomp(mtcars[,c(1:7,10,11)], center = TRUE,scale. = TRUE)
#view a summary of principle components
summary(mtcars.pca)

library(devtools)
install_github("vqv/ggbiplot")

library(ggbiplot)

ggbiplot(mtcars.pca)

ggbiplot(mtcars.pca, labels=rownames(mtcars))