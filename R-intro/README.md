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


