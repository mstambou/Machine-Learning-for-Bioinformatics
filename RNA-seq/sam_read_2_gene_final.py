# -*- coding: utf-8 -*-
"""
Created on Fri Sep 07 15:28:34 2018

@author: mstambou

script I made that will read in a sam file and will get map reads to genes
genes to reads to calculate coverage and abundance

this script is only for metagenomics samples and does not account for differential
expressions.
The way the abundance is calculated is that it takes for each genome (or contig) or gene
it takes all the reads mapped to it and divides it by the total number of reads and divides it
by the length of the gene/genome/contig. Hence it is normalized. If we want to average the abundance 
of lets say one genome which is made from many contigs you just take the average of all the 
abundances from the different contigs, you dont have to normalize after this step since it's allready 
been normalized by the lengths of the contigs.

Run example:
    python sam_read_2_gene.py dir/to/sam/example.sam dir/to/out/example.out
"""

import sys
import re

class genome:
    def __init__(self):
        #length of the genome
        self.genome_length = 0
        #list of tuples read IDs and lengths for those that are mapped to more than one genome
        self.multimapped_read_id_and_lengths = list()
        #total number of reads mapped back to this genome(unique and multiple)
        self.total_nreads_mapped = 0
        #keeps a count of the total number of shotgun fragments mapped to the genome
        #fragements are used for paired end sequencing. when two reads from a pair are mapped to
        #to a single gene concordantly these are considered as one fragment and should not be 
        #counted twice.
        self.n_fragments = 0
        #a dictionary of tuples where the key will be common read name without the pair number and the 
        #tuple value will be the full key name 
        self.fragment_dic = dict()
        #list of fragments that are uniquely mapped to this gene/ome
        self.unique_fragments = list()
        #list of fragments that are mapped to this and other gene/genomes
        self.multi_fragments = list()
        #abundance calcualted soley from the unique hits to this gene/genome
        self.unique_abundance = float()
        #unique ebundance per million kilobase
        self.unique_abundance_pmkb = float()
        #abundance value calculated from the set of fragments that are multimapped between this genome/gene and other genomes/genes.
        self.multi_abundance = float()
        self.multi_abundance_pmkb = float()
        #total abundance of the gene/genome that is calulated using the unique reads(fragments) and multi-reads(fragments)
        self.abundance = float()
        self.abundance_pmkb = float()
        #fragnebts per million
        self.fpkm = float()
        #total length of reads mapped to genome
        self.total_read_id_and_lengths = list()        
        #list of tuples for unique reads only
        self.unique_read_id_and_lengths = list()
        #records the final coverage of the genome using unique and multimapped reads
        self.coverage = float()
    #adds a tuple of the read ID and the length of the mapped read    
    def add_total_map(self, tup):
        self.total_read_id_and_lengths.append(tup)
    def split_unique_multi_reads(self, read_dic):
        for tup in self.total_read_id_and_lengths:
            if read_dic[tup[0]].n_maps == 1:
                self.unique_read_id_and_lengths.append(tup)
            elif read_dic[tup[0]].n_maps > 1:
                self.multimapped_read_id_and_lengths.append(tup)
    def add_fragment(self, frag_common_id, frag_1, frag_2):        
        if frag_common_id in self.fragment_dic:
            self.fragment_dic[frag_common_id].append((frag_1, frag_2))
        else:
            self.fragment_dic[frag_common_id] = [(frag_1,frag_2)]
    def get_unique_reads(self):        
        return self.unique_read_id_and_lengths
    def get_multi_reads(self):
        return self.multimapped_read_id_and_lengths
    def avg_read_length(self):
        return (self.total_read_length/self.total_nreads_mapped)
    def avg_unique_read_length(self):
        if len(self.unique_read_id_and_lengths) > 0:
            return (sum([unique_tup[1] for unique_tup in self.unique_read_id_and_lengths])/float(len(self.unique_read_id_and_lengths)))
        return 0.0
    def avg_multi_read_length(self):
        if len(self.multimapped_read_id_and_lengths) > 0:
            return (sum([multi_tup[1] for multi_tup in self.multimapped_read_id_and_lengths]))/float(len(self.multimapped_read_id_and_lengths))
        return 0.0
    
        
class reads:
    def __init__(self):
        #list of genes that the read is mapped to
        self.genomes = list()
        self.length = int()
        #object variable keeps count of the number of times the read is being mapped to a reference
        self.n_maps = int()
        self.genome_location_pair = list()
        #a dictionary where the key is genome_id, and 2nd is the length of the alignment between the read and the reference segment
        self.read_genome_map_len_dic = dict()
        #keeps track of the genome and the location in the genome(ome) that the read maps to
    def add_genome_loc_pair(self, tup): 
        self.genome_location_pair.append(tup)
    def get_gen_loc_pairs(self):
        return self.genome_location_pair
    def add_read_genome_map_dic(self, genome_id, map_length):
        self.read_genome_map_len_dic[genome_id] = map_length
    #dictionary that contains the genome id as key and the length of the mapping for this read to that genome.
    def get_read_genome_map_dic(self):
        return self.read_genome_map_len_dic
     
class fragments:
    def __init__(self):
        self.genomes = list()
        self.read_pair_tuple_list = list()
        #a dictionary for gene/geneome specific coefficient for all the multireads, keys are genome IDs
        #values are genome specific coefficients
        self.genome_specific_multi_read_coefficient = dict()
        self.genome_specific_multi_read_coefficient_pmkb = dict()
        

def get_read_common_id(read_id):
    return '.'.join(read_id.split('.')[:-1])

def get_ref_aln_len(cigar_string):
    mlen, ins, dele, clip, ref_alnlen = 0, 0, 0, 0, 0
    match = re.findall(r"([0-9]+)([A-Z]+)", cigar_string)    
    for amatch in match:
        d, c = int(amatch[0]), amatch[1]        
        if c == 'M':
            mlen += d
        elif c == 'I':
            ins += d
        elif c == 'D':
            dele += d
        elif c == 'S':
             clip += d		  
    ref_alnlen = mlen + dele
   
    return ref_alnlen

def get_binary(flag):
    return '{0:012b}'.format(int(flag))

##start reading the sam file
    
def read_sam():
    
    genome_dic = dict()
    read_dic = dict()
    fragment_dic = dict()
    prev_read = ''
    mate_count = 0
    #sam_in = 'sample_sam/SRR769540_multi_maped_mapped_only.sam'
    with open(sys.argv[1], 'r') as in_f:
        for row in in_f:
            if row.startswith('@SQ'):
                row = row.split('\t')
                #get the name of the gene/genome and store it in dictionary
                genome_id = row[1][3:]
                #create a genome instance at that dictionary entry
                genome_dic[genome_id] = genome()
                #add the length of the whole genome to that dictionary entry
                genome_dic[genome_id].genome_length = int(row[2][3:])
            #now when you start going row by row through the reads
            elif not row.startswith('@'):
                row = row.split('\t')

                #if the read has no mapping to the reference or if it doesnt align at all then skip
                if row[2] != '*' and row[5] != '*': #makes sure that the read is mapped to a reference
                    read_id = row[0]
                    genome_id = row[2]
                    common_read_id = read_id.split('::')[-1]
            #function I defined that will caluclate the length of the read mapped from the CIGAR feature
                    map_length = get_ref_aln_len(row[5])
                    if read_id not in read_dic:
                        read_dic[read_id] = reads()
                        #add the length of the read only once (the first time you encoutner that read)
                        #since your assuming the same read is present as the same length in the multiple occurances
                        read_dic[read_id].length = len(row[9])
                    if common_read_id not in fragment_dic:
                        fragment_dic[common_read_id] = fragments()
                    if genome_id not in read_dic[read_id].genomes:
                        read_dic[read_id].genomes.append(genome_id)
                        
                    read_dic[read_id].add_genome_loc_pair((genome_id, int(row[3])))
                    read_dic[read_id].n_maps += 1
                    read_dic[read_id].add_read_genome_map_dic(genome_id,  map_length)
                    genome_dic[genome_id].total_nreads_mapped += 1
                    genome_dic[genome_id].add_total_map((read_id, map_length))
                    #assign fragments to genes/genomes taking into account their paired end nature
                    binary_flag = get_binary(row[1])
                    if prev_read.split('::')[-1] != read_id.split('::')[-1]:
                        mate_count = 0
                    if binary_flag[-3] == '0': #read is mapped
                        
                        if binary_flag[-1] == '1': #read is paied
                            mate_count += 1
                            if mate_count!=0 and mate_count%2==0:
                                mate = True
                            elif mate_count%2 == 1:
                                mate = False
                            if binary_flag[-4] == '0': #mate is also mapped                                
                                if prev_read.split('::')[-1] == read_id.split('::')[-1] and mate == True:                                     
                                    fragment_dic[common_read_id].genomes.append(genome_id)
                                    if binary_flag[-7] == '1':#first in pair
                                        genome_dic[genome_id].add_fragment(common_read_id, read_id, prev_read)
                                        fragment_dic[common_read_id].read_pair_tuple_list.append((read_id, prev_read))
                                        genome_dic[genome_id].n_fragments += 1
                                    else: #else the current is second in pair previous is first in pair
                                        genome_dic[genome_id].add_fragment(common_read_id, prev_read, read_id)
                                        fragment_dic[common_read_id].read_pair_tuple_list.append((prev_read, read_id))
                                        genome_dic[genome_id].n_fragments += 1
                            elif binary_flag[-4] == '1': #mate unmapped                   
                                fragment_dic[common_read_id].genomes.append(genome_id)
                                if binary_flag[-7] == '1':#first in pair
                                    genome_dic[genome_id].add_fragment(common_read_id, read_id, 'nan')
                                    fragment_dic[common_read_id].read_pair_tuple_list.append((read_id, 'nan'))
                                    genome_dic[genome_id].n_fragments += 1
                                else:# else if its mate is unmapped and its the second read
                                    genome_dic[genome_id].add_fragment(common_read_id, 'nan', read_id)
                                    fragment_dic[common_read_id].read_pair_tuple_list.append(('nan', read_id))
                                    genome_dic[genome_id].n_fragments += 1
                        if binary_flag[-1] == '0': #read is unpaired
                            fragment_dic[common_read_id].genomes.append(genome_id)
                            if binary_flag[-8] == '1':#second in pair with an unmapped mate
                                genome_dic[genome_id].add_fragment(common_read_id, 'nan', read_id)
                                fragment_dic[common_read_id].read_pair_tuple_list.append(('nan', read_id))
                                genome_dic[genome_id].n_fragments += 1
                            else:#first in pair with unmapped mate
                                genome_dic[genome_id].add_fragment(common_read_id, read_id, 'nan')
                                fragment_dic[common_read_id].read_pair_tuple_list.append((read_id, 'nan'))
                                genome_dic[genome_id].n_fragments += 1
                                                    
                    prev_read = read_id


    return genome_dic, read_dic, fragment_dic

def get_coverage(genome_dic, genome_id, read_dic):
    genome_dic[genome_id].split_unique_multi_reads(read_dic)
    n_unique_reads_tup = len(genome_dic[genome_id].get_unique_reads())
    avg_unique_reads_len = genome_dic[genome_id].avg_unique_read_length()
    multi_read_tup = genome_dic[genome_id].get_multi_reads()    
    coverage = 0.0
    coverage = n_unique_reads_tup*avg_unique_reads_len
    #for each multiread, the coverage is the length of the alignment between the read and the genome divided the number of times the read is mapped to genomes
    for multi_read in multi_read_tup:
        #get_read_genome_map_dic is a dictionaty that has genome (or gene) ID as the key and the length of mapping between read and genome or gene as value
        coverage += read_dic[multi_read[0]].get_read_genome_map_dic()[genome_id]/float(read_dic[multi_read[0]].n_maps)
    coverage = coverage / float(genome_dic[genome_id].genome_length)
    return coverage

def set_unique_multi_fragments(genome_id, genome_dic, fragment_dic):
    """
    function that will extract the uniquely mapped fragments, which later will be 
    used to calculate the fpkm
    """
    genome_fragments = genome_dic[genome_id].fragment_dic.keys()
    for fragment in genome_fragments:
        #I added this step so that fragments mapped to the same genome twice are still
        #considered as unique maps.
        fragment_dic[fragment].genomes = list(set(fragment_dic[fragment].genomes))
        if len(fragment_dic[fragment].genomes) == 1:
            genome_dic[genome_id].unique_fragments.append(fragment)
        else:
            genome_dic[genome_id].multi_fragments.append(fragment)
            
def set_specific_coeff(genome_dic, fragment_dic):
    """
    for each gene or genome set its specific coeficient, based on the qin et al. paper 
    for defining gene/genome specific coefficients. This is based on the multimapped fragments
    """
    for genome_id in genome_dic:        
        #get all the fragments for this genome that are multimapped also with other genomes
        for multi_frag in genome_dic[genome_id].multi_fragments:
            #get list of genomes that this particular fragment is multimapped to
            multi_frag_genomes = fragment_dic[multi_frag].genomes
            multi_hit_genomes_abundance = 0.0 #/SUM{Ab(U)}
            multi_hit_genomes_abundance_pmkb = 0.0 
            for multi_genome_id in multi_frag_genomes:                
                multi_hit_genomes_abundance += genome_dic[multi_genome_id].unique_abundance            
                multi_hit_genomes_abundance_pmkb += genome_dic[multi_genome_id].unique_abundance_pmkb
            if not genome_dic[genome_id].unique_fragments:
                fragment_dic[multi_frag].genome_specific_multi_read_coefficient[genome_id] = 1.0/len(multi_frag_genomes)
                fragment_dic[multi_frag].genome_specific_multi_read_coefficient_pmkb[genome_id] = 1.0/len(multi_frag_genomes)
            else:                                                                                                                               #/SUM(Ab(u))
                fragment_dic[multi_frag].genome_specific_multi_read_coefficient[genome_id] = (genome_dic[genome_id].unique_abundance)/(float(multi_hit_genomes_abundance))
                fragment_dic[multi_frag].genome_specific_multi_read_coefficient_pmkb[genome_id] = (genome_dic[genome_id].unique_abundance_pmkb)/(float(multi_hit_genomes_abundance_pmkb))
           
def set_abundance(genome_dic, fragment_dic):
    """
    void function that will calculate the total abundance for a gene/genome
    based on the definition defined in qin 2014, using the abundance from unique
    and multiple hit fragments
    """
    for genome_id in genome_dic:
        #if not genome_dic[genome_id].unique_fragments:
            #continue
        genome_unique_abundance = genome_dic[genome_id].unique_abundance
        genome_unique_abundance_pmkb = genome_dic[genome_id].unique_abundance_pmkb
        genome_multi_abundance = 0.0
        genome_multi_abundance_pmkb = 0.0
        for multi_frag in genome_dic[genome_id].multi_fragments:
            genome_multi_abundance += fragment_dic[multi_frag].genome_specific_multi_read_coefficient[genome_id]
            genome_multi_abundance_pmkb += fragment_dic[multi_frag].genome_specific_multi_read_coefficient_pmkb[genome_id]
        genome_multi_abundance = genome_multi_abundance/(genome_dic[genome_id].genome_length)
        genome_multi_abundance_pmkb = genome_multi_abundance_pmkb/((genome_dic[genome_id].genome_length)/1000.0)#genome length in kilobase
        genome_dic[genome_id].multi_abundance = genome_multi_abundance
        genome_dic[genome_id].multi_abundance_pmkb = genome_multi_abundance_pmkb
        genome_dic[genome_id].abundance = genome_unique_abundance + genome_multi_abundance
        genome_dic[genome_id].abundance_pmkb = genome_unique_abundance_pmkb + genome_multi_abundance_pmkb
        
def get_pm_scaling_factor(genome_dic):
    """
    void function that calculates the per million scaling factor for the reads sample.
    this will consider only the reads that are actually mapped
    """
    total_fragments = 0
    for genome_id in genome_dic:
        total_fragments += genome_dic[genome_id].n_fragments
    per_million_scaling_factor = total_fragments/float(10**6)
    return per_million_scaling_factor


if len(sys.argv) != 3:
    print ('please enter name of sam input file and name of output file; i.e python sam_read_2_gene.py dir/to/sam/example.sam dir/to/out/example.out')
else:
    genome_dic, read_dic, fragment_dic = read_sam()
    per_million_scaling_factor = get_pm_scaling_factor(genome_dic)
    for genome_id in genome_dic:
        #print (genome_id)
        genome_dic[genome_id].coverage = get_coverage(genome_dic, genome_id, read_dic)
        set_unique_multi_fragments(genome_id, genome_dic, fragment_dic)
        genome_dic[genome_id].unique_abundance = len(genome_dic[genome_id].unique_fragments)/float(genome_dic[genome_id].genome_length)
        genome_dic[genome_id].unique_abundance_pmkb = (len(genome_dic[genome_id].unique_fragments)/(per_million_scaling_factor))/(float(genome_dic[genome_id].genome_length/1000.0))
    
    set_specific_coeff(genome_dic, fragment_dic)
    set_abundance(genome_dic, fragment_dic)

    out_f = open(sys.argv[2], 'w')
    out_f.write('genome_id\tcoverage\tuniq_abundance\tmulti_abundance\ttotal_abundance\ttotal_abundance_pmkb\n')    
    for genome_id in genome_dic:
        out_f.write(genome_id+'\t'+str(genome_dic[genome_id].coverage)+'\t' + str(genome_dic[genome_id].unique_abundance) + '\t'+str(genome_dic[genome_id].multi_abundance) +'\t'+ str(genome_dic[genome_id].abundance)+'\t'+str(genome_dic[genome_id].abundance_pmkb)+'\n')
    out_f.close()
