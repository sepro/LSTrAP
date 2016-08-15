import configparser
import time
import os

from cluster.templates import build_template, build_batch_template


class PipelineBase:
    def __init__(self, config, data, enable_log=False):
        """
        Constructor run with path to ini file with settings

        :param config: path to setttings ini file
        """
        self.cp = configparser.ConfigParser()
        self.cp.read(config)

        self.dp = configparser.ConfigParser()
        self.dp.read(data)

        self.trimmomatic_path = self.cp['TOOLS']['trimmomatic_path']

        self.blast_module = None if self.cp['TOOLS']['blast_module'] is 'None' else self.cp['TOOLS']['blast_module']
        self.bowtie_module = None if self.cp['TOOLS']['bowtie_module'] is 'None' else self.cp['TOOLS']['bowtie_module']
        self.tophat_module = '' if self.cp['TOOLS']['tophat_module'] is 'None' else self.cp['TOOLS']['tophat_module']
        self.samtools_module = None if self.cp['TOOLS']['samtools_module'] is 'None' else self.cp['TOOLS']['samtools_module']
        self.python_module = None if self.cp['TOOLS']['python_module'] is 'None' else self.cp['TOOLS']['python_module']
        self.python3_module = None if self.cp['TOOLS']['python3_module'] is 'None' else self.cp['TOOLS']['python3_module']
        self.interproscan_module = None if self.cp['TOOLS']['interproscan_module'] is 'None' else self.cp['TOOLS']['interproscan_module']
        self.mcl_module = None if self.cp['TOOLS']['mcl_module'] is 'None' else self.cp['TOOLS']['mcl_module']

        self.bowtie_build_cmd = self.cp['TOOLS']['bowtie_cmd']
        self.trimmomatic_se_cmd = self.cp['TOOLS']['trimmomatic_se_command']
        self.trimmomatic_pe_cmd = self.cp['TOOLS']['trimmomatic_pe_command']
        self.tophat_se_cmd = self.cp['TOOLS']['tophat_se_cmd']
        self.tophat_pe_cmd = self.cp['TOOLS']['tophat_pe_cmd']
        self.htseq_count_cmd = self.cp['TOOLS']['htseq_count_cmd']
        self.interproscan_cmd = self.cp['TOOLS']['interproscan_cmd']
        self.orthofinder_cmd = self.cp['TOOLS']['orthofinder_cmd']

        self.pcc_cmd = self.cp['TOOLS']['pcc_cmd']
        self.mcl_cmd = self.cp['TOOLS']['mcl_cmd']
        self.mcxdeblast_cmd = self.cp['TOOLS']['mcxdeblast_cmd']

        self.genomes = self.dp['GLOBAL']['genomes'].split(';')
        self.email = None if self.dp['GLOBAL']['email'] == 'None' else self.cp['DEFAULT']['email']

        self.enable_log = enable_log

        if self.enable_log:
            self.log = open('rstrap.log', 'w')
        else:
            self.log = None

    def __exit__(self, exc_type, exc_value, traceback):
        if self.enable_log:
            self.log.close()

    def write_submission_script(self, jobname, module, command, filename):
        """
        Writes a job submission script that includes a timestamp, required to keep track if a job is running or not

        :param jobname: name of the job include %d for the timestamp !
        :param module: Module to load, separate multiple modules using spaces in case more than one module is required
        :param command: The command to execute, separate multiple commands using newlines
        :param filename: filename for the script include %d for the timestamp !
        :return: tuple with stamped_filename and stamped_jobname
        """
        timestamp = int(time.time())
        stamped_filename = str(filename % timestamp)
        stamped_jobname = str(jobname % timestamp)

        template = build_template(stamped_jobname, self.email, module, command)

        with open(stamped_filename, "w") as f:
            print(template, file=f)

        return stamped_filename, stamped_jobname

    def write_batch_submission_script(self, jobname, module, command, filename, jobcount=100):
        """
        Writes a job submission script that includes a timestamp, required to keep track if a job is running or not

        :param jobname: Name of the job include %d for the timestamp !
        :param module: Module to load, separate multiple modules using spaces in case more than one module is required
        :param command: The command to execute, separate multiple commands using newlines
        :param filename: Filename for the script include %d for the timestamp !
        :param jobcount: Number of jobs included in the batch (default = 100)
        :return: Tuple with stamped_filename and stamped_jobname
        """
        timestamp = int(time.time())
        stamped_filename = str(filename % timestamp)
        stamped_jobname = str(jobname % timestamp)

        template = build_batch_template(stamped_jobname, self.email, module, command, jobcount)

        with open(stamped_filename, "w") as f:
            print(template, file=f)

        return stamped_filename, stamped_jobname

    @staticmethod
    def clean_out_files(jobname):
        """
        Concatenates output of jobs into a single log file and removes the individual files

        :param jobname: name of the job
        """

        def write_log(files, log):
            """
            Function to concatenate files into a log

            :param files: list of file to concatenate
            :param log: filename of the log
            """
            if len(files) > 0:
                with open(log, "w") as f_out:
                    for f in files:
                        with open(f, "r") as f_in:
                            for l in f_in:
                                f_out.write(l)

        out_log = jobname + '.out.log'
        err_log = jobname + '.err.log'

        out_files = []
        err_files = []

        for file in os.listdir('./'):
            if file.startswith('OUT_'+jobname+'.'):
                out_files.append(file)
            elif file.startswith('ERR_'+jobname+'.'):
                err_files.append(file)

        write_log(out_files, out_log)
        write_log(err_files, err_log)

        for f in out_files + err_files:
            os.remove(f)
