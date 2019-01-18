#installing R packages
install.packages("fdrtool") # need to specify the package name; this command installs "fdrtool"

#after installing you can load/use the package by:
library(fdrtool)

#loading data:
mydata <- read.csv("http://www.ats.ucla.edu/stat/data/binary.csv")

#There are built in datasets in R that come with the standard library and could be used to run/test algorithms
#for example the airquality dataset:
data(airquality)
summary(airquality)# to get an idea about what the data contains

#working with data in R.
#data frames are a popular data strcutre used to store data in tabualr format in R.
#let's create our own data frame.
n = c(2, 3, 5) 
s = c("aa", "bb", "cc") 
b = c(TRUE, FALSE, TRUE) 
df = data.frame(n, s, b)
#we can merge two dataframe into each other either by row or colums
df1 = data.frame(name=c("Hunter", "Ethan", "Paolo", "Crystal"), age=c(9, 8, 9, 3))
df2 = data.frame(name=c("Aiden", "Evan"), age=c(9, 8))
df = rbind(df1, df2)
#we can access feature i.e. columns of dataframes using the $ key.
#to add a column to the dataframe:
df$school = "Rogers"
#another datastrcture in R is a list
data_list = list()
data_list[[1]] = data.frame(name=c("Hunter", "Ethan", "Paolo", "Crystal"), age=c(9, 8, 9, 3))
data_list[[2]] = data.frame(name=c("Aiden", "Evan"), age=c(9, 8))
data_list[1] #lists could be indexed


#R also supports many indexing techniques
y[3]  #third element
y[3:7]  #from third to 7th elements
y[c(3, 5, 6, 9)]  #3rd, 5th, 6th, and 9th elements
y[-1]  #drop the first element; dropping using negative ingegers
y[y > 6] #all the elements that are > 6


#you can query dataframes and select rows and columns based on logical conditions
#for example get the indivduals that are 8 years or older
df = data.frame(name=c("Hunter", "Ethan", "Paolo", "Crystal"), age=c(9, 8, 9, 3))
df_sub = subset(df, age>=8)




