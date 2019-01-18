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
