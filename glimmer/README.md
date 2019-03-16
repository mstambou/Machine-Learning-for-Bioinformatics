This week's lab is going to be focused on a bioinformatics tool called 'GLIMMER'. Glimmer is a tool that is used in finding/predicting genes in microbial DNA, especially genomes of bactera, archaea and viruses. Glimmer is short for gene Locator and Interpolated Markov ModelER), evident from the name uses interpolated Markov models. (IMMs) to identify coding regions (CDS) of the dna and discriminate them from non-coding regions. Usually coding DNA regions (or RNA), code for proteins, i.e. DNA gets transcribed to RNA which in tunr gets translated to a sequence of amino acids and fold into it's appropriate protein. A basic requirement for this process to happen is a start and a stop codon at the begining and the end of the coding sequences respectively. 

Glimmer is based on markov models, which has proven to be effective in finding genes. However defining a kth order markov model might not work in certain cases depending on the size of our observations that we have to train the model. There is often a debate to make K larger to generalize more which in turn would need much more observations or make k smaller which would however lose sensitivity.

Glimmer on the other hand uses some generalization of a Markov Chain, in particular this generalization is called interpolated context model, which was first termed by the authors who created glimmer. For further details about the implimentation of glimmer and how it works, these references would be recommended:
* [Glimmer webpage](http://ccb.jhu.edu/software/glimmer/index.shtml)
* [Glimmer manual](http://ccb.jhu.edu/software/glimmer/glim302notes.pdf)
* [lecture notes about Glimmer](https://courses.cs.washington.edu/courses/cse527/00wi/lectures/lect14.pdf)
* [Glimmer paper 1](https://www.ncbi.nlm.nih.gov/pubmed/10556321)
* [Glimmer paper 2](https://www.ncbi.nlm.nih.gov/pubmed/9421513)

Glimmer is allready preinstalled on SICE servers, to use it all we have to do is to load it as a module, i.e.
```
module load glimmer
```

## Using Glimmer

1. Building the model using `build-icm`
    * Using known genes
    * Using long, non-overlapping ORFs (using `long-orfs`)
    * Using genes from a highly similar species.
 2. Predicting genes using `glimmer3`
