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

Let us use the sample files provided with Glimmer package, to practice on how to run the program.

  * [Treponema pallidium genome](tpall.fna)
  * [List of annotated genes](tpall.nh)
  
### Build a model from scratch
Running Glimmer is a two-step process. First, a probability model of coding sequences,
called an interpolated context model or ICM, must be built. This is done by the program
build-icm from a set of training sequences

We first find long, overlapping ORFs in the genome using `long-orfs`.
Note that :

`USAGE: long-orfs [options] <sequence-file> <output-file>`

So we can issue the following command on bash :

`long-orfs -n -t 1.15 tpall.fna orf-list.nh`

Which will generate `orf-list.nh`.
Examine this file using cat.
Now we need to extract the training sequences from the genome using `extract`. Note that :

`USAGE:  extract [options] <sequence-file> <coords>`

So we can do  :

`extract -t tpall.fna orf-list.nh > orf-seq.fna`

Which will generate orf-seq.fna.
Examine this file using cat.
We will then build the model based on this training set using `build-icm`.
Note that :   

`USAGE:  build-icm [options] output_file < input-file`

So we can do :

`build-icm -r orf-model.icm < orf-seq.fna`

Which will generate the file `orf-model.icm`.
Examine this file with cat.
Now we can predict other genes in our genome using `glimmer3`. Note that :

`USAGE:  glimmer3 [options] <sequence-file> <icm-file> <tag>`

So we can do :

`glimmer3 tpall.fna orf-model.icm orfBased`

Which will generate files `orfBased.predict` and `orfBased.detail`.
Examine these with cat.

### Build a model using known genes

Building the model from scratch is the worst case scenario.
In most cases, a lot of genes may be easily identified using homology searches.
We have a list of such genes in [tpall.nh](tpall.nh) and we can use them instead of the long ORF sequences we found.
This is likely to yield better results in most occasions.

Start by examining `tpall.nh` with cat.
Then we can extract the sequences for these genes by doing :

`extract -t tpall.fna tpall.nh > gene-seq.fna`

Build the model by doing :

`build-icm -r gene-model.icm < gene-seq.fna`

Predict more genes by doing :

`glimmer3 tpall.fna gene-model.icm geneBased`

Examine the resulting files `geneBased.predict` and `geneBased.detail` to see how your results differ from the previous run.

#### Combining training sets

Do you think combining the long orfs you found using `long-orfs` with the genes you found by homology searches a good idea?

Do that as an excercise and see how your results differ.

