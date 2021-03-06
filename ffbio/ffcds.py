#!/usr/bin/env python3

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, FileType
from signal import SIG_DFL, SIGPIPE, signal

from Bio import SeqIO


def parse_cds(stream):
    for record in SeqIO.parse(stream, "genbank"):
        for feature in record.features:
            if feature.type == "CDS":
                protein_id = feature.qualifiers["protein_id"][0]
                product = feature.qualifiers.get("product", ["n/a"])[0]
                cds = feature.extract(record)
                cds.id = protein_id
                cds.description = f"{record.id}|{feature.location} {product}"
                yield cds


def parse_argv(argv):
    parser = ArgumentParser(
        description="extract CDS sequence records from a GenBank file",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("file", type=FileType(), help="the sequence file")

    args = parser.parse_args(argv)

    return args


def main(argv):
    args = parse_argv(argv[1:])
    with args.file as stream:
        SeqIO.write(parse_cds(stream), sys.stdout, "fasta")


if __name__ == "__main__":
    signal(SIGPIPE, SIG_DFL)
    sys.exit(main(sys.argv))
