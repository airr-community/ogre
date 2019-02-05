# Copyright William Lees
#
# This source code, and any executable file compiled or derived from it, is governed by the European Union Public License v. 1.2,
# the English version of which is available here: https://perma.cc/DK5U-NDVE
#

# Calculate statistics based on published genotypes

from collections import OrderedDict

from Bio import SeqIO
from app import db

from db.submission_db import *
from db.gene_description_db import *
from imgt.imgt_ref import imgt_reference_genes


def parse_name(name):
    allele_designation = ''
    subgroup_designation = ''
    gene_subgroup = ''
    sn = name

    if '-' in sn:
        if '*' in sn:
            snq = sn.split('*')
            allele_designation = snq[1]
            sn = snq[0]
        else:
            allele_designation = ''
        snq = sn.split('-')
        subgroup_designation = snq[len(snq)-1]
        del(snq[len(snq)-1])
        gene_subgroup = '-'.join(snq)[4:]
    elif '*' in sn:
        snq = sn.split('*')
        gene_subgroup = snq[0][4:]
        allele_designation = snq[1]
    else:
        gene_subgroup = sn[4:]

    if len(subgroup_designation) == 1:
        subgroup_designation = '0' + subgroup_designation

    if len(allele_designation) == 1:
        allele_designation = '0' + allele_designation

    return(gene_subgroup, subgroup_designation, allele_designation)


def generate_stats(species, locus, sequence_type, min_freq, min_occ):
    imgt_ref = imgt_reference_genes()
    if species not in imgt_ref:
        return (0, None)

    ref = []

    for gene in imgt_ref[species].keys():
        if locus in gene and gene[3] == sequence_type:
            ref.append(gene)

    # Get unique list of genotype descriptions that underlie affirmed inferences

    genotype_descriptions = []
    seqs = db.session.query(GeneDescription).filter(GeneDescription.status == 'published',
                                                    GeneDescription.organism == species,
                                                    GeneDescription.locus == locus,
                                                    GeneDescription.sequence_type == sequence_type,
                                                    GeneDescription.affirmation_level != '0'
                                                    ).all()

    for seq in seqs:
        for genotype in seq.inferred_sequences:
            if genotype.genotype_description not in genotype_descriptions:
                genotype_descriptions.append(genotype.genotype_description)

    if len(genotype_descriptions) == 0:
        return (0, None)

    # Initialise stats

    stats = {}

    for name in ref:
        stats[name] = {'occurrences': 0, 'unmutated_freq': [], 'gene': name}

    stats = OrderedDict(sorted(stats.items(), key=lambda name: parse_name(name[0])[2]))
    stats = OrderedDict(sorted(stats.items(), key=lambda name: parse_name(name[0])[1]))
    stats = OrderedDict(sorted(stats.items(), key=lambda name: parse_name(name[0])[0]))

    # Compose stats

    for desc in genotype_descriptions:
        for gen in desc.genotypes:
            if gen.sequence_id in stats and gen.unmutated_frequency >= min_freq:
                stats[gen.sequence_id]['occurrences'] += 1
                stats[gen.sequence_id]['unmutated_freq'].append(gen.unmutated_frequency)

    for (k, stat) in stats.items():
        stats[k]['unmutated_freq'] = round(sum(stat['unmutated_freq'])/max(len(stat['unmutated_freq']),1), 2)

    ret = []
    for(k, stat) in stats.items():
        if stats[k]['occurrences'] >= min_occ:
            ret.append(stat)

    return (len(genotype_descriptions), ret)
