## RNA-seq Data
In this lab we are going to be introduced to gene expression data obtaine by RNA-seq, using next generation sequencing techniques. In this particular case the data is obtianed by Illumina HiSeq 2500 machine. This will produce [paired end reads](https://www.illumina.com/science/technology/next-generation-sequencing/paired-end-vs-single-read-sequencing.html). 
Here we are extracting gene expression data for Escherichia coli str. K-12 species. There are in total 6 sequencing [samples](https://www.ncbi.nlm.nih.gov/sra/?term=Escherichia+coli+str.+K-12+RNA+seq), but for now we are only going to extract 3 of them. You can extract the raw reads in [fastq](https://en.wikipedia.org/wiki/FASTQ_format) format by going to the [EBI](https://www.ebi.ac.uk/) website and simply pasting the sample accession numbers there. For todays experiment we're extracting sequence data with the following accessions:
* SRR8309842
* SRR8309843
* SRR8309844

The typical steps taken to obtain these raw reads RNA-seq data are:
1) deciding on library types, sequencing depth, number of replicates etc.
2) Extracting the RNA seqs, preparing libraries.
These processes generate short reads in fastq format, such as the ones that we are going to deal with today. 
Following these steps comes data preparation and analysis, which we will be going through today. These steps include:
1) quality control: seeing if the reads are of high quality and postprocessing them if needed (trimming etc)
2) mapping the reads to a reference sequence (in our case, or to contigs in other cases), using some maping tool
3) quantification of abundance of these genes.
4) differential expression analysis.

