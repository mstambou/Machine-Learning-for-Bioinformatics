R is a programming environment for statistical computing and graphics.
It is not as practical as Python for general purpose programming, but very intuitive to use for statistical computing.

#### Installing R

R is installed on all SoIC computers (i.e. silo, tank) so you can start it by typing `R`.
R is also available as a module on IU clusters (i.e. [Karst](https://www.datacamp.com/)) and can be loaded by typing `module load curl java r`.

If you need to install R on your oen computer, you download it [here](https://cloud.r-project.org/).
[CRAN](https://cran.r-project.org/) is a repository which you can use to install many R packages.
This is similiar to the pip (or conda) package management system of Python.
The [Bioconductor](https://bioconductor.org) project provides a lot of bioinformatics related tools beyond what is available in CRAN.

[RStudio](https://www.rstudio.com/) provides a graphical environment for R, much like Spyder for Python.
You can also use R with Jupyter notebooks after installing the [R kernel for Jupyter](https://github.com/IRkernel/IRkernel).

#### Using R

R is not my favorite environment but it is very easy to get going and very practical for certain tasks.
The real strength of R comes from data structures that were designed with statistical computing in mind (note that [pandas](http://pandas.pydata.org/) offers R-like data structures for Python.), and the CRAN/Bioconductor ecosystem which has community supported tools for many common applications.

To familiarize yourself with the R syntax, I recomend you quickly run through the [DataCamp](https://www.datacamp.com/) introductory tutorial.

Now, let us run through the short tutorial that I inherited from the previous years lab notes :

One of the reasons R became a popular language is because of the wide community eactively developing usefull packages for analysis and visualization. CRAN (Comprehensive R Archive Network) has made it easy to install packages in R. To install a package that you need to use you simply include:
```R
install.packages("package_name")
library(package_name)
```


### Loading some data

If you cloned this repository, you should already have [binary.csv](binary.csv).

We can read data using one of the read functions, in this case because we have a csv file on hand, we can do `read.csv("binary.csv")`.
But this merely reads and prints the data.
We would rather store it in a variable, so try `data <- read.csv("binary.csv")`.

you can also directly read the same dataset from its online repositiry by issuing the following command:

```R
mydata <- read.csv("http://www.ats.ucla.edu/stat/data/binary.csv")
```
Lets practice some R syntax using this [script](R_intro.R) on the repository

R also provides built in datasets in R that come with the standard library and could be used to run/test algorithms
for example the airquality dataset
### working with data
data frames are a popular data strcutre used to store data in tabualr format in R. let's create our own data frame.
* we can merge two dataframe into each other either by row or colums
* we can access feature i.e. columns of dataframes using the $ key
* we can add a column to the dataframe

Lists are another datastrcture in R that are used a lot.
* we can index lists in many different ways


Like we did in the case of lists, we can also query dataframes and select rows and columns based on logical conditions for example get the indivduals that are 8 years or older

### Plotting data in R

Plotting is made easy in R once you get used to the syntax. R has a lot of libraries to produce fancy plots but for now let's just stick to the basics. In R there are:
* High-level plotting functions create a new plot on the graphics device, possibly with axes, labels, titles and so on.
* Low-level plotting functions add more information to an existing plot, such as extra points, lines and labels.
* Interactive graphics functions allow you interactively add information to, or extract information from, an existing plot, using a pointing device such as a mouse.

Lets use the air passengers dataset and plots some histograms and line plots.

Another widely used plot is the boxplot.
* Box plots display variation in samples of a statistical population without making any assumptions of the underlying statistical distribution. The spacings between the different parts of the box indicate the degree of dispersion (spread) and skewness in the data, and show outliers. 
* R command: boxplot()
* By default, boxplot() automatically computes median, first and third quartile ("hinges") and 95% confidence interval of median ("notches").

Lets do a box plot on the same air passengers dataset, and study the distribution of cholesterol levels across three different types of individuals (non-smokers, pipe smokers and cigar smokers).
We can see some differences in the average levels of the cholesterol across these thre groups.

### Clustering
Clustering is a commonly used techinique in any type of analysis especially if we do not have much information about our dataset and we want to see some patterns and check whether or not our data is organized to some extent. We're going to apply two popular clustering techniques over small datasets to demonstrate their results. Let's follow this [script](R_clustering.R) to practice some clustering

#### Hierarchical CLustering

A popular family of clustering algorithms are the [hierarchical based clustering](https://en.wikipedia.org/wiki/Hierarchical_clustering), especially used in phylogenetics. This type of clustering builds a tree relationship among the cells and user can decide on a horizontal line to choose the granularity of clustering. There are also choices concerning the distance metric and agglomeration method that is needed to be made. In this case we will resort to wards method for agglomeration, which merges two clusters by minimizing some objective function (such as reducing the intra cluster distance or maximizing the inter-cluster distance).

Let's first synthesize a dataset in R in order to run a hierarchical clustering.
Results in Hierarchical clustering can be visualized in nice dendograms. 
Let's cluster the cars dataset also using this type of clustering.

Let's get a classification data set from UCI repository. We're going to use the breast cancer dataset, where thei patients are classified as malignent or benign based on certain featureand characteristics of their cells and physiology. Ideally one would expect two good clusters from this dataset.
Since this is a non-supervised learning we should ommit the class column otherwise clustering would be made too easy in this case.

#### K-means clustering

 
 [K-means](https://en.wikipedia.org/wiki/K-means_clustering) clustering aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean, serving as a prototype of the cluster. The value of K is user provided and is usually decide after some trial and error. 
 
 * A popular method to decide on the number of cluster in k-means is using the elbow method. This is demonstrated in the code, we first plot the sum of errors within groups as a function of number of clusters we want to cluster. 
 *Naturally the error will decrease as we increase the number of clusters, but a reasonable choice of cluster numbers is when we see the biggest drop in error values.
 * In this case we're setting the number of cluster to be 5.
 
 ### Dimensionality reductions and Principle Component Analysis
 
 Principal Component Analysis (PCA) is a useful technique for exploratory data analysis, allowing you to better visualize the variation present in a dataset with many variables. It is particularly helpful in the case of "wide" datasets, where you have many variables for each sample. In this tutorial, you'll discover PCA in R.
 
 #### Usefullness 
 Imagine a dataset where many variables are present (High dimensional data), you cannot easily plot the data in its raw format, making it difficult to get a sense of the trends present within. PCA allows you to see the overall "shape" of the data, identifying which samples are similar to one another and which are very different. This can enable us to identify groups of samples that are similar and work out which variables make one group different from another.
 
 #### How it works
 What PCA does is it takes a dataset with many variables, and you simplify that dataset by turning your original variables into a smaller number of "Principal Components". rincipal Components are the underlying structure in the data. They are the directions where there is the most variance, the directions where the data is most spread out. This means that we try to find the straight line that best spreads the data out when it is projected along it. This is the first principal component, the straight line that shows the most substantial variance in the data. 
 It's a linear transformation of your dataset, to a new coordinate system in such a way that the most significant variance is found on the first coordinate, and each subsequent coordinate is orthogonal to the last and has a lesser variance. In this way, you transform a set of x correlated variables over y samples to a set of p uncorrelated principal components over the same samples. 
 Where many variables correlate with one another, they will all contribute strongly to the same principal component. Each principal component sums up a certain percentage of the total variation in the dataset. Where your initial variables are strongly correlated with one another, you will be able to approximate most of the complexity in your dataset with just a few principal components
 
 #### PCA example 
 Here we will put PCA for a test by applying it on the "mtcars" dataset that we've allready seen before. As we saw the dataset has 32 car models and each car has 11 features. Since PCA is a linear transformation of our feature space and it works well with numerical data, lets first clean our dataset and remvoe all the columns that contain categorical datas. This leaves us with a 9x32 matrix.
 
 Let's apply the PCA algorithm on our data and what each PC represents.
 The results show that:
 * we obtain 9 principal components, which you call PC1-9. 
 * Each of these explains a percentage of the total variation in the dataset. That is to say: PC1 explains 63% of the total variance, which means that nearly two-thirds of the information in the dataset (9 variables) can be encapsulated by just that one Principal Component. 
 * PC2 explains 23% of the variance. So, by knowing the position of a sample in relation to just PC1 and PC2, you can get a very accurate view on where it stands in relation to other samples, as just PC1 and PC2 can explain 86% of the variance.
 
 #### Plotting PCA
 Let us plot our PCA. You will make a biplot, which includes both the position of each sample in terms of PC1 and PC2 and also will show you how the initial variables map onto this.
  * we're going use the ggbiplot package, for this slightly more advanced plot, which offers a user-friendly and pretty function to plot biplots. 
  * A biplot is a type of plot that will allow you to visualize how the samples relate to one another in our PCA (which samples are similar and which are different) and will simultaneously reveal how each variable contributes to each principal component.
  Let's first install the necesarry packages.
  
  The X-axis and Y-axis in the plot rerpresent out first and second principal components. We also can see their labels that show the percentage of variance each of these PCs capture in the data.
  The red axes are seen as arrows originating from the center point. Here, we see that the variables hp, cyl, and disp all contribute to PC1, with higher values in those variables moving the samples to the right on this plot. This lets us see how the data points relate to the axes.
  
  Now let's label the data points on the graph in order to see which of these rows are clustered together along the principal components.
 
