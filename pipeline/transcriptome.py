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
            if 'fastq_dir' in self.dp[g]:
                fastq_input_dir = self.dp[g]['fastq_dir']
                trimmed_output = self.dp[g]['trimmomatic_output']
                os.makedirs(trimmed_output, exist_ok=True)

                fastq_files = []

                for file in os.listdir(fastq_input_dir):
                    if file.endswith('.fq.gz') or file.endswith('.fastq.gz'):
                        fastq_files.append(file)

                # sort required to make sure _1 files are before _2
                fastq_files.sort()

                while len(fastq_files) > 0:
                    file = fastq_files.pop(0)

                    if '_1.' in file:
                        pair_file = file.replace('_1.', '_2.')
                        if pair_file in fastq_files:
                            fastq_files.remove(pair_file)
                            print('Submitting pair %s, %s' % (file, pair_file))
                        else:
                            print('Submitting single %s' % file)
                            outfile = file.replace('.fq.gz', '.trimmed.fq.gz') if file.endswith('.fq.gz') else file.replace('.fastq.gz', '.trimmed.fastq.gz')
                            subprocess.call(["qsub", "-v", "in=" + os.path.join(fastq_input_dir, file) + ",out=" + os.path.join(trimmed_output, outfile), filename_se])
                    else:
                        print('Submitting single %s' % file)
                        outfile = file.replace('.fq.gz', '.trimmed.fq.gz') if file.endswith('.fq.gz') else file.replace('.fastq.gz', '.trimmed.fastq.gz')
                        subprocess.call(["qsub", "-v", "in=" + os.path.join(fastq_input_dir, file) + ",out=" + os.path.join(trimmed_output, outfile), filename_se])

        print('Trimming fastq files...')

        # wait for all jobs to complete
        wait_for_job(jobname)

        # remove the submission script
        os.remove(filename_se)
        os.remove(filename_pe)

        print("Done\n\n")





