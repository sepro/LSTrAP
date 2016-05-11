import sys

__bad_fields = ['no_feature', 'ambiguous', 'too_low_aQual', 'not_aligned', 'alignment_not_unique']


def htseq_count_quality(filename, cutoff=1, log=None):
    print("checking quality of htseq-count")
    values = []
    total_count = 0

    with open(filename, "r") as fin:
        for l in fin:
            gene, count = l.strip().split('\t')
            if all([bf not in gene for bf in __bad_fields]):
                values.append(int(count))
                total_count += int(count)

    if total_count == 0:
        print("N50 check for", filename, "failed. No reads found")
        return False

    values.sort(reverse=True)

    # write lengths to log file !
    if log is not None:
        current_count = 0
        for e, v in enumerate(values, start=1):
            current_count += v
            if current_count > total_count / 2:
                print('N50 found', e, file=log)
                break

    current_count = 0
    for e, v in enumerate(values, start=1):
        current_count += v
        if current_count > total_count/2:
            if e >= cutoff:
                print(filename, e, cutoff, current_count, total_count, len(values))
                return True

            break

    print("N50 check for", filename, "failed.", e, cutoff)
    return False






