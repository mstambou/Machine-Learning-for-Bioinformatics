#ref: https://jef.works/blog/2018/06/28/single-cell-clustering-comparison/

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("sva", version = "3.8")

set.seed(0)
#to install MUDAN follow git repo: https://github.com/JEFworks/MUDAN
install.packages("devtools")
require(devtools)
devtools::install_github("JEFworks/MUDAN")
library(MUDAN)
data(pbmcB)
## filter out poor genes and cells, weeds out the underrepresented genes, the ones that dont have a lot of reads mapped to it
cd <- cleanCounts(pbmcB, 
                  min.reads = 10, 
                  min.detected = 10, 
                  verbose=FALSE)

## CPM normalization, depth normalized counts as opposed to TPM (length normalized, by gene length)
mat <- normalizeCounts(cd, 
                       verbose=FALSE) 
## variance normalize, identify overdispersed genes
matnorm.info <- normalizeVariance(mat, 
                                  details=TRUE, 
                                  verbose=FALSE,
                                  alpha=0.2) 

## log transform
matnorm <- log10(matnorm.info$mat+1) 
## dimensionality reduction on overdispersed genes
pcs <- getPcs(matnorm[matnorm.info$ods,], 
              nGenes=length(matnorm.info$ods), 
              nPcs=30, 
              verbose=FALSE) 
## get tSNE embedding  (is a non-linear dimensionality reduction, similar objects are modeled by nearby points dissimalar are modeled by far away points)
emb <- Rtsne::Rtsne(pcs, 
                    is_distance=FALSE, 
                    perplexity=30, 
                    num_threads=parallel::detectCores(), 
                    verbose=FALSE)$Y 
rownames(emb) <- rownames(pcs)

#Based on our prior knowledge of marker genes, we can already tell that there must be distinct clusters corresponding to
#B-cells, T-cells subtypes, monocytes, and so forth. Indeed, we can see that CD20 (MS4A1) expression marks a distinct group
#of cells, presumably B-cells. And similarly, CD3E marks our T-cells, and so forth.

par(mfrow=c(3,3), mar=rep(2,4))
markers <- c('MS4A1', 'CD3E', 'IL7R', 'CCR7', 'CD8A', 'FCGR3A', 'CD14', 'HLA-DRA', "XCL1")
invisible(lapply(markers, function(g) {
  # plot binarized expression (on or off)
  plotEmbedding(emb, colors=(cd[g,]>0)*1, 
                main=g, xlab=NA, ylab=NA, 
                verbose=FALSE) 
}))

## k-means
set.seed(0)
com.km <- kmeans(pcs, centers=10)$cluster
par(mfrow=c(1,1), mar=rep(2,4))
plotEmbedding(emb, com.km, 
              main='K-Means', xlab=NA, ylab=NA, 
              mark.clusters=TRUE, alpha=0.1, mark.cluster.cex=1,
              verbose=FALSE) 


## Hierarchical DBSCAN
install_github("mhahsler/dbscan")
library(dbscan)
set.seed(0)
com.db <- hdbscan(pcs[,1:5], minPts=5)$cluster
names(com.db) <- rownames(pcs)
par(mfrow=c(1,1), mar=rep(2,4))
plotEmbedding(emb, com.db, 
              main='HDBSCAN', xlab=NA, ylab=NA, 
              mark.clusters=TRUE, alpha=0.1, mark.cluster.cex=1,
              verbose=FALSE)


