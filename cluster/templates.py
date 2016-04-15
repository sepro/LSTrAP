

__template = """#!/bin/bash
#

#$ -N %s
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -o OUT_$JOB_NAME.$JOB_ID
#$ -e ERR_$JOB_NAME.$JOB_ID

#email
%s

#
%s
date
hostname
%s
date
"""


def build_template(name, email, module, cmd):
    include_email = "" if email is None else "#$ -m bea\n#$ -M " + email
    load_module = "" if module is None else "module load " + module

    return __template % (name, include_email, load_module, cmd)
