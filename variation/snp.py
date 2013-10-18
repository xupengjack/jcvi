#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Analyze SNPs in resequencing panels.
"""

import sys
import logging

from jcvi.formats.fasta import Fasta
from jcvi.apps.base import OptionParser, ActionDispatcher, debug
debug()


def main():

    actions = (
        ('frommaf', 'Convert to four-column tabular format from MAF'),
            )
    p = ActionDispatcher(actions)
    p.dispatch(globals())


def frommaf(args):
    """
    %prog frommaf maffile

    Convert to four-column tabular format from MAF.
    """
    p = OptionParser(frommaf.__doc__)
    p.add_option("--validate",
                 help="Validate coordinates against FASTA [default: %default]")
    opts, args = p.parse_args(args)

    if len(args) != 1:
        sys.exit(not p.print_help())

    maf, = args
    snpfile = maf.rsplit(".", 1)[0] + ".vcf"
    fp = open(maf)
    fw = open(snpfile, "w")
    total = 0
    id = "."
    qual = 20
    filter = "PASS"
    info = "DP=20"
    print >> fw, "##fileformat=VCFv4.0"
    print >> fw, "#CHROM POS ID REF ALT QUAL FILTER INFO".replace(" ", "\t")
    for row in fp:
        atoms = row.split()
        c, pos, ref, alt = atoms[:4]
        try:
            c = int(c)
        except:
            continue
        c = "chr{0:02d}".format(c)
        pos = int(pos)
        print >> fw, "\t".join(str(x) for x in \
                (c, pos, id, ref, alt, qual, filter, info))
        total += 1
    fw.close()

    validate = opts.validate
    if not validate:
        return

    from jcvi.utils.cbook import percentage

    f = Fasta(validate)
    fp = open(snpfile)
    nsnps = 0
    for row in fp:
        if row[0] == '#':
            continue

        c, pos, id, ref, alt, qual, filter, info = row.split("\t")
        pos = int(pos)
        feat = dict(chr=c, start=pos, stop=pos)
        s = f.sequence(feat)
        s = str(s)
        assert s == ref, "Validation error: {0} is {1} (expect: {2})".\
                        format(feat, s, ref)
        nsnps += 1
        if nsnps % 50000 == 0:
            logging.debug("SNPs parsed: {0}".format(percentage(nsnps, total)))
    logging.debug("A total of {0} SNPs validated and written to `{1}`.".\
                        format(nsnps, snpfile))


if __name__ == '__main__':
    main()