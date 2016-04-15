import configparser
import time
import subprocess

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
        bowtie_module = self.cp['TOOLS']['bowtie_module']
        bowtie_build_cmd = self.cp['TOOLS']['bowtie_cmd']

        genomes = self.dp['GLOBAL']['genomes'].split(';')
        email = None if self.dp['GLOBAL']['email'] == 'None' else self.cp['DEFAULT']['email']

        # Filename should include a unique timestamp !
        filename = "bowtie_build_%d.sh" % int(time.time())

        template = build_template("bowtie_build", email, bowtie_module, bowtie_build_cmd)

        with open(filename, "w") as f:
            print(template, file=f)

        for g in genomes:
            con_file = self.dp[g]['genome_fasta']
            output = self.dp[g]['bowtie_output']

            print("in=" + con_file + ",out=" + output)

            subprocess.call(["qsub", "-v", "in=" + con_file + ",out=" + output, filename])

        print("Preparing the genomic fasta file...")

        wait_for_job(filename)

        print("Done\n\n")

    def process_fastq(self):
        print("Processing fastq files")

        filename = ""

        wait_for_job(filename)

        print("Done\n\n")

    def run(self):
        self.prepare_genome()

        # self.process_fastq()




