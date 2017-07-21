import re

quality_fields = ['__no_feature', '__ambiguous', '__too_low_aQual', '__not_aligned', '__alignment_not_unique']


def check_tophat(filename, cutoff=0, log=None):
    """
    Checks the alignment summary of TopHat's output, if it passes it returns true, else false
    Optionally information can be written to a log file

    :param filename: align_summary.txt to check
    :param cutoff: If the percentage of mapped reads is below this the sample won't pass (default= 0, no check)
    :param log: filehandle to write log to, set to None for no log
    :return: True if the sample passed, false otherwise
    """

    re_mapped = re.compile('Mapped   :.*\(\s*(.*)% of input\)')

    with open(filename, 'r') as f:
        lines = '\t'.join(f.readlines())
        hits = re_mapped.search(lines)
        if hits:
            value = float(hits.group(1))
            if value >= cutoff:
                return True
            else:
                if log is not None:
                    print('WARNING:', filename, 'didn\'t pass alignment check!', value, 'reads mapped. Cutoff,',
                          cutoff, file=log)

    return False


def check_hisat2(filename, cutoff=0, log=None):
    """
    Checks the alignment summary of TopHat's output, if it passes it returns true, else false
    Optionally information can be written to a log file

    :param filename: align_summary.txt to check
    :param cutoff: If the percentage of mapped reads is below this the sample won't pass (default= 0, no check)
    :param log: filehandle to write log to, set to None for no log
    :return: True if the sample passed, false otherwise
    """

    # 93.77% overall alignment rate
    re_mapped = re.compile('(.*)% overall alignment rate')

    with open(filename, 'r') as f:
        lines = '\t'.join(f.readlines())
        hits = re_mapped.search(lines[-1])
        if hits:
            value = float(hits.group(1))
            if value >= cutoff:
                return True
            else:
                if log is not None:
                    print('WARNING:', filename, 'didn\'t pass alignment check!', value, 'reads mapped. Cutoff,',
                          cutoff, file=log)


    return False


def check_htseq(filename, cutoff=0, log=None):
    """
    Checks the mapping statistics in htseq files how many reads map into coding sequences. If the percentage is high
    enough it will return True, otherwise false. Optionally additional information can be written to log

    :param filename: htseq-file to check
    :param cutoff: If the percentage of mapped reads is below this the sample won't pass (default= 0, no check)
    :param log: filehandle to write log to, set to None for no log
    :return: True if the sample passed, false otherwise
    """
    values = {}

    with open(filename) as fin:
        mapped_reads = 0
        for line in fin:
            gene, value = line.strip().rsplit(maxsplit=1)

            if gene not in quality_fields:
                mapped_reads += int(value)
            else:
                values[gene] = int(value)

        total = sum([mapped_reads,
                     values['__no_feature'] if '__no_feature' in values.keys() else 0,
                     values['__ambiguous'] if '__ambiguous' in values.keys() else 0]
                    )

        percentage_mapped = ((mapped_reads*100)/total) if total > 0 else 0

        if percentage_mapped >= cutoff:
            return True
        else:
            if log is not None:
                print('WARNING:', filename, 'didn\'t pass HTSEQ-Count Quality check!', percentage_mapped
                      , 'reads mapped. Cutoff,', cutoff, file=log)

    return False
