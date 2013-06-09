#!/usr/bin/env python

import os;
from pyphylogenomics import OrthoDB
from pyphylogenomics import BLAST
from pyphylogenomics import MUSCLE


"""
We will find all single-copy genes for the silk moth Bombyx mori using the table
from OrthoDB as input file:
"""
in_file = 'data/OrthoDB6_Arthropoda_tabtext.csv'
genes = OrthoDB.single_copy_genes(in_file, 'Bombyx mori')


"""
Pull all sequences for our gene IDs from the CDS file and write them to a file
pulled_seqs.fa:
"""
cds_file = "data/silkcds.fa"
BLAST.get_cds(genes, cds_file)
print "File moved to data/pulled_seqs.fa"
os.rename("pulled_seqs.fa", "data/pulled_seqs.fa")


"""
Do a BLASTn of the sequences against the Bombyx mori genome. The input arguments
are your file containing the sequences for single-copy genes (pulled_seqs.fa) 
and your file with the genome of Bombyx mori which is in FASTA format (silkgenome.fa).
"""
##BLAST.blastn('data/pulled_seqs.fa', 'data/silkgenome.fa')


"""
As stated before, we prefer long exons for each of the candidate genes ( > 300
nucleotides):
"""
exons = BLAST.getLargestExon("data/pulled_seqs_blastn_out.csv", E_value=0.001, ident=98, exon_len=300)


"""
Some small segments of sequences might be similar to non-homologous regions of
the genome. We will use the function eraseFalsePosi to keep those matches of
longest length:
"""
exons = BLAST.eraseFalsePosi(exons) # Drop presumable false positives.


"""
Ideally we want exons that are not too close to each other in the genome to
avoid gene linkage. So we will keep only those exons that are apart by 810
kilobases:
"""
exons = BLAST.wellSeparatedExons(exons) # Keep exons separated by > 810KB


"""
Finally we can use a function to save the obtained exons while making sure they
are in frame. We need to use as additional arguments the genome file and output
filename:
"""
BLAST.storeExonsInFrame(exons, "data/pulled_seqs.fa", "data/Bombyx_exons.fas")


"""
    Validation of exon structure

Do a blastn of our Long Exons against the Danaus genome:
"""
BLAST.blastn("data/Bombyx_exons.fas", "data/Dp_genome_v2.fasta");


"""
We need to parse the output blast table and extract the exons from Danaus that
are longer than 300bp and are homologous to the exons of Bombyx mori.
"""
BLAST.blastParser("data/Bombyx_exons_blastn_out.csv", "data/Dp_genome_v2.fasta", "data/Danaus_exons.fas", sp_name="Danaus")


"""
BLASTn the Bombyx mori exons against the Heliconius genome:
"""
BLAST.blastn("data/Bombyx_exons.fas", "data/Heliconius_genome.fa");


"""
Parse the blast table, extract the exon sequences and save them to a file:
"""
BLAST.blastParser("data/Bombyx_exons_blastn_out.csv", "data/Heliconius_genome.fa",
                "data/Heliconius_exons.fas", sp_name="Heliconius")


"""
Blasted the Bombyx mori exons against the Manduca genome
"""
BLAST.blastn("data/Bombyx_exons.fas", "data/Msex05162011.genome.fa")


"""
Parsing the output blast table:
"""
BLAST.blastParser("data/Bombyx_exons_blastn_out.csv", "data/Msex05162011.genome.fa", 
                "data/Manduca_exons.fas", sp_name="Manduca")

"""
Do alignment of homologous exons across several taxa
"""
files = ["data/Bombyx_exons.fas", "data/Danaus_exons.fas", "data/Heliconius_exons.fas",
                "data/Manduca_exons.fas"];
MUSCLE.batchAlignment(files);
