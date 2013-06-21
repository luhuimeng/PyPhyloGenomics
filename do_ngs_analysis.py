#!/usr/bin/env python

import glob;
import os;

# prepare raw NGS data for analysis
from pyphylogenomics import NGS;

ionfile = "ionrun.fastq";
#NGS.prepare_data(ionfile); # file is written to data/modified/wrk_ionfile.fasta



# find reads matching target genes using BLAST
from pyphylogenomics import BLAST;

query_seqs = "data/modified/wrk_ionfile.fasta";
genome = "target_genes.fasta";
#BLAST.blastn(query_seqs, genome); # blast results saved as wrk_ionfile_blast_out.csv

blast_table = "data/modified/wrk_ionfile_blastn_out.csv";
sbj_db      = "data/modified/wrk_ionfile.fastq";
#NGS.parse_blast_results(blast_table, sbj_db);



# find reads matching our indexes and do separation
# we will take a list of indexes corresponding to individuals 
# and use it to separate the gene bins 
index_list = "indexes.fasta";
folder = "output";
levenshtein_distance = 0;
for gene_file in glob.glob(os.path.join("output", "gene*fastq")):
    NGS.separate_by_index(gene_file, index_list, folder, levenshtein_distance);