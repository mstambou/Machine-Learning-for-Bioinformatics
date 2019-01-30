
pdf(file = "heatmap.pdf", width = 12, height = 14, family = "Helvetica", pointsize = 12)
par(mar=c(8, 10, 10, 10))

abundances = read.table('all_samples_abundance.txt', sep = '\t', header = TRUE)

abundances_mat <- abundances[,-1]
rownames(abundances_mat) <- abundances[,1]

abundances_mat = abundances_mat[600:700,]

heatmap(as.matrix(abundances_mat),
        scale="column",
        col=heat.colors(256),
        main='diferential gene expression',
        Rowv=NA,
        Colv=NA)
dev.off()