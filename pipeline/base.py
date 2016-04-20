import configparser
import time
from cluster.templates import build_template, build_batch_template


class PipelineBase:
    def __init__(self, config, data):
        """
        Constructor run with path to ini file with settings

        :param config: path to setttings ini file
        """
        self.cp = configparser.ConfigParser()
        self.cp.read(config)

        self.dp = configparser.ConfigParser()
        self.dp.read(data)

        self.bowtie_module = None if self.cp['TOOLS']['bowtie_module'] is 'None' else self.cp['TOOLS']['bowtie_module']
        self.tophat_module = '' if self.cp['TOOLS']['tophat_module'] is 'None' else self.cp['TOOLS']['tophat_module']
        self.samtools_module = None if self.cp['TOOLS']['samtools_module'] is 'None' else self.cp['TOOLS']['samtools_module']
        self.python_module = None if self.cp['TOOLS']['python_module'] is 'None' else self.cp['TOOLS']['python_module']
        self.interproscan_module = None if self.cp['TOOLS']['interproscan_module'] is 'None' else self.cp['TOOLS']['interproscan_module']

        self.bowtie_build_cmd = self.cp['TOOLS']['bowtie_cmd']
        self.trimmomatic_se_cmd = self.cp['TOOLS']['trimmomatic_se_command']
        self.trimmomatic_pe_cmd = self.cp['TOOLS']['trimmomatic_pe_command']
        self.tophat_se_cmd = self.cp['TOOLS']['tophat_se_cmd']
        self.tophat_pe_cmd = self.cp['TOOLS']['tophat_pe_cmd']
        self.samtools_cmd = self.cp['TOOLS']['samtools_cmd']
        self.htseq_count_cmd = self.cp['TOOLS']['htseq_count_cmd']
        self.interproscan_cmd = self.cp['TOOLS']['interproscan_cmd']

        self.genomes = self.dp['GLOBAL']['genomes'].split(';')
        self.email = None if self.dp['GLOBAL']['email'] == 'None' else self.cp['DEFAULT']['email']

    def write_submission_script(self, jobname, module, command, filename):
        timestamp = int(time.time())
        stamped_filename = str(filename % timestamp)
        stamped_jobname = str(jobname % timestamp)

        template = build_template(stamped_jobname, self.email, module, command)

        with open(stamped_filename, "w") as f:
            print(template, file=f)

        return stamped_filename, stamped_jobname

    def write_batch_submission_script(self, jobname, module, command, filename, jobcount=100):
        timestamp = int(time.time())
        stamped_filename = str(filename % timestamp)
        stamped_jobname = str(jobname % timestamp)

        template = build_batch_template(stamped_jobname, self.email, module, command, jobcount)

        with open(stamped_filename, "w") as f:
            print(template, file=f)

        return stamped_filename, stamped_jobname
