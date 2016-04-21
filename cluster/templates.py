

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

__batch_template = """#!/bin/bash
#

#$ -N %s
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -t 1-%d

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
    """
    Generates submit script for a normal job.

    :param name: Name for the job
    :param email: Email address of the user, set to None to disable email
    :param module: Module to load, separate multiple modules using spaces in case more than one module is required
    :param cmd: The command to execute, separate multiple commands using newlines
    :return: The completed template
    """
    include_email = "" if email is None else "#$ -m bea\n#$ -M " + email
    load_module = "" if module is None else "module load " + module

    return __template % (name, include_email, load_module, cmd)


def build_batch_template(name, email, module, cmd, jobs):
    """
    Generates submit script for a batch job.

    :param name: Name for the job
    :param email: Email address of the user, set to None to disable email
    :param module: Module to load, separate multiple modules using spaces in case more than one module is required
    :param cmd: The command to execute, separate multiple commands using newlines
    :param jobs: Number of jobs to include in the batch file
    :return: The completed template
    """
    include_email = "" if email is None else "#$ -m bea\n#$ -M " + email
    load_module = "" if module is None else "module load " + module

    return __batch_template % (name, jobs, include_email, load_module, cmd)