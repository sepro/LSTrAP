import re
import sys

from subprocess import check_output, DEVNULL
from time import sleep


def detect_cluster_system():
    """
    Checks which cluster manager is installed on the system, return "SGE" for Sun/Oracle Grid Engine, "PBS" for
    PBS/Torque based systems and otherwise "other"

    :return: string "SBE", "PBS" or "other"
    """

    try:
        which_output = check_output(["which", "sge_qmaster"], stderr=DEVNULL).decode("utf-8")

        if "/sge_qmaster" in which_output:
            return "SGE"
    except Exception as _:
        pass

    try:
        which_output = check_output(["which", "pbs_sched"], stderr=DEVNULL).decode("utf-8")

        if "/pbs_sched" in which_output:
            return "PBS"
    except Exception as _:
        pass

    return "other"


def job_running(job_name):
    """
    Checks if a specific job is still running on a cluster using the qstat command

    :param job_name: name of the submitted script/jobname
    :return: boolean true if the job is still running or in the queue
    """

    running_jobs = []
    c_system = detect_cluster_system()

    if c_system == "SGE":
        # Sun/Oracle Grid engine detected
        qstat = check_output(["qstat", "-r"]).decode("utf-8")

        pattern = "Full jobname:\s*" + job_name

        running_jobs = re.findall(pattern, qstat)
    elif c_system == "PBS":
        # Sun/Oracle Grid engine detected
        qstat = check_output(["qstat", "-f"]).decode("utf-8")
        pattern = "Job_Name = \s*" + job_name
        running_jobs = re.findall(pattern, qstat)
    else:
        print("Unsupported System", file=sys.stderr)

    if len(running_jobs) > 0:
        print('Still %d jobs running.' % len(running_jobs), end='\r')
    else:
        print('\nDone!\n')

    return bool(len(running_jobs) > 0)


def wait_for_job(job_name, sleep_time=5):
    """
    Checks if a job is running and sleeps for a set number of minutes if it is

    :param job_name: name of the job to check
    :param sleep_time: time to sleep between polls (in minutes, default = 5)
    """
    while job_running(job_name):
        sleep(sleep_time*60)
