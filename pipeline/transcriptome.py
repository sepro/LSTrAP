import configparser
import time
import subprocess
import os

from cluster import wait_for_job
from cluster.templates import build_template


class TranscriptomePipeline:
    """
    TranscriptomePipeline class. Reads a settings ini file and runs the transcriptome pipeline
    """
    def __init__(self, config, data):
        """
        Constructor run with path to ini file with settings

        :param config: path to setttings ini file
        """
        self.cp = configparser.ConfigParser()
        self.cp.read(config)

        self.dp = configparser.ConfigParser()
        self.dp.read(data)

    def prepare_genome(self):
        """
        Runs bowtie-build for each genome on the cluster. All settings are obtained from the settings fasta file
        """
        bowtie_module = None if self.cp['TOOLS']['bowtie_module'] is 'None' else self.cp['TOOLS']['bowtie_module']
        bowtie_build_cmd = self.cp['TOOLS']['bowtie_cmd']

        genomes = self.dp['GLOBAL']['genomes'].split(';')
        email = None if self.dp['GLOBAL']['email'] == 'None' else self.cp['DEFAULT']['email']

        # Filename should include a unique timestamp !
        timestamp = int(time.time())
        filename = "bowtie_build_%d.sh" % timestamp
        jobname = "bowtie_build_%d" % timestamp

        template = build_template(jobname, email, bowtie_module, bowtie_build_cmd)

        with open(filename, "w") as f:
            print(template, file=f)

        for g in genomes:
            con_file = self.dp[g]['genome_fasta']
            output = self.dp[g]['bowtie_output']

            print("in=" + con_file + ",out=" + output)

            subprocess.call(["qsub", "-v", "in=" + con_file + ",out=" + output, filename])

        print("Preparing the genomic fasta file...")

        # wait for all jobs to complete
        wait_for_job(jobname)

        # remove the submission script
        os.remove(filename)

        print("Done\n\n")

    def trim_fastq(self):
        trimmomatic_se_cmd = self.cp['TOOLS']['trimmomatic_se_command']
        trimmomatic_pe_cmd = self.cp['TOOLS']['trimmomatic_pe_command']

        genomes = self.dp['GLOBAL']['genomes'].split(';')
        email = None if self.dp['GLOBAL']['email'] == 'None' else self.cp['DEFAULT']['email']

        # Filename should include a unique timestamp !
        timestamp = int(time.time())
        filename_se = "trimmomatic_se_%d.sh" % timestamp
        filename_pe = "trimmomatic_pe_%d.sh" % timestamp
        jobname = "trimmomatic_%d" % timestamp

        template_se = build_template(jobname, email, None, trimmomatic_se_cmd)
        template_pe = build_template(jobname, email, None, trimmomatic_pe_cmd)

        with open(filename_se, "w") as f:
            print(template_se, file=f)

        with open(filename_pe, "w") as f:
            print(template_pe, file=f)

        for g in genomes:
            fastq_input_dir = self.dp[g]['fastq_dir']

        print("Trimming fastq files...")

        # wait for all jobs to complete
        wait_for_job(jobname)

        # remove the submission script
        os.remove(filename_se)
        os.remove(filename_pe)

        print("Done\n\n")





