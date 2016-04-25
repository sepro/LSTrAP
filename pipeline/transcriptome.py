import subprocess
import os

from cluster import wait_for_job
from utils.matrix import read_matrix, write_matrix, normalize_matrix_counts, normalize_matrix_length
from pipeline.base import PipelineBase


class TranscriptomePipeline(PipelineBase):
    """
    TranscriptomePipeline class. Reads a settings ini file and runs the transcriptome pipeline
    """
    def prepare_genome(self):
        """
        Runs bowtie-build for each genome on the cluster. All settings are obtained from the settings fasta file
        """
        filename, jobname = self.write_submission_script("bowtie_build_%d",
                                                         self.bowtie_module,
                                                         self.bowtie_build_cmd,
                                                         "bowtie_build_%d.sh")

        for g in self.genomes:
            con_file = self.dp[g]['genome_fasta']
            output = self.dp[g]['bowtie_output']

            os.makedirs(os.path.dirname(output), exist_ok=True)

            subprocess.call(["qsub", "-v", "in=" + con_file + ",out=" + output, filename])

        print("Preparing the genomic fasta file...")

        # wait for all jobs to complete
        wait_for_job(jobname)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def trim_fastq(self):
        """
        Runs Trimmomatic on all fastq files
        """
        filename_se, jobname = self.write_submission_script("trimmomatic_%d",
                                                            None,
                                                            self.trimmomatic_se_cmd,
                                                            "trimmomatic_se_%d.sh")
        filename_pe, jobname = self.write_submission_script("trimmomatic_%d",
                                                            None,
                                                            self.trimmomatic_pe_cmd,
                                                            "trimmomatic_pe_%d.sh")

        for g in self.genomes:
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

                        ina = os.path.join(fastq_input_dir, file)
                        inb = os.path.join(fastq_input_dir, pair_file)

                        outap = file.replace('.fq.gz', '.trimmed.paired.fq.gz') if file.endswith('.fq.gz') else file.replace('.fastq.gz', '.trimmed.paired.fastq.gz')
                        outau = file.replace('.fq.gz', '.trimmed.unpaired.fq.gz') if file.endswith('.fq.gz') else file.replace('.fastq.gz', '.trimmed.unpaired.fastq.gz')

                        outbp = pair_file.replace('.fq.gz', '.trimmed.paired.fq.gz') if pair_file.endswith('.fq.gz') else pair_file.replace('.fastq.gz', '.trimmed.paired.fastq.gz')
                        outbu = pair_file.replace('.fq.gz', '.trimmed.unpaired.fq.gz') if pair_file.endswith('.fq.gz') else pair_file.replace('.fastq.gz', '.trimmed.unpaired.fastq.gz')

                        outap = os.path.join(trimmed_output, outap)
                        outau = os.path.join(trimmed_output, outau)

                        outbp = os.path.join(trimmed_output, outbp)
                        outbu = os.path.join(trimmed_output, outbu)

                        print('Submitting pair %s, %s' % (file, pair_file))
                        subprocess.call(["qsub", "-v", "ina=%s,inb=%s,outap=%s,outau=%s,outbp=%s,outbu=%s" % (ina, inb, outap, outau, outbp, outbu), filename_pe])
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
        wait_for_job(jobname, sleep_time=1)

        # remove the submission script
        os.remove(filename_se)
        os.remove(filename_pe)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def run_tophat(self):
        """
        Maps the reads from the trimmed fastq files to the bowtie-indexed genome
        """
        filename_se, jobname = self.write_submission_script("tophat_%d",
                                                            self.bowtie_module + ' ' + self.tophat_module,
                                                            self.tophat_se_cmd,
                                                            "tophat_se_%d.sh")

        filename_pe, jobname = self.write_submission_script("tophat_%d",
                                                            self.bowtie_module + ' ' + self.tophat_module,
                                                            self.tophat_pe_cmd,
                                                            "tophat_pe_%d.sh")

        print('Mapping reads with tophat...')

        for g in self.genomes:
            tophat_output = self.dp[g]['tophat_output']
            bowtie_output = self.dp[g]['bowtie_output']
            trimmed_fastq_dir = self.dp[g]['trimmomatic_output']
            os.makedirs(tophat_output, exist_ok=True)

            pe_files = []
            se_files = []

            for file in os.listdir(trimmed_fastq_dir):
                if file.endswith('.paired.fq.gz') or file.endswith('.paired.fastq.gz'):
                    pe_files.append(file)
                elif not (file.endswith('.unpaired.fq.gz') or file.endswith('.unpaired.fastq.gz')):
                    se_files.append(file)

            # sort required to make sure _1 files are before _2
            pe_files.sort()
            se_files.sort()

            for pe_file in pe_files:
                if '_1.trimmed.paired.' in pe_file:
                    pair_file = pe_file.replace('_1.trimmed.paired.', '_2.trimmed.paired.')

                    output_dir = pe_file.replace('_1.trimmed.paired.fq.gz', '').replace('_1.trimmed.paired.fastq.gz', '')
                    output_dir = os.path.join(tophat_output, output_dir)
                    forward = os.path.join(trimmed_fastq_dir, pe_file)
                    reverse = os.path.join(trimmed_fastq_dir, pair_file)
                    print('Submitting pair %s, %s' % (pe_file, pair_file))
                    subprocess.call(["qsub", "-v", "out=%s,genome=%s,forward=%s,reverse=%s" % (output_dir, bowtie_output, forward, reverse), filename_pe])

            for se_file in se_files:
                print('Submitting single %s' % se_file)
                output_dir = se_file.replace('.trimmed.fq.gz', '').replace('.trimmed.fastq.gz', '')
                output_dir = os.path.join(tophat_output, output_dir)
                subprocess.call(["qsub", "-v", "out=%s,genome=%s,fq=%s" % (output_dir, bowtie_output, os.path.join(trimmed_fastq_dir, se_file)), filename_se])

        # wait for all jobs to complete
        wait_for_job(jobname, sleep_time=1)

        # remove the submission script
        os.remove(filename_se)
        os.remove(filename_pe)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def run_samtools(self):
        """
        Convert tophat output (bam file) to sam file
        """
        filename, jobname = self.write_submission_script("samtools_%d",
                                                         self.samtools_module,
                                                         self.samtools_cmd,
                                                         "samtools_%d.sh")

        for g in self.genomes:
            tophat_output = self.dp[g]['tophat_output']
            samtools_output = self.dp[g]['samtools_output']
            os.makedirs(samtools_output, exist_ok=True)

            dirs = [o for o in os.listdir(tophat_output) if os.path.isdir(os.path.join(tophat_output, o))]
            for d in dirs:
                bam_file = os.path.join(tophat_output, d, 'accepted_hits.bam')
                if os.path.exists(bam_file):
                    sam_file = os.path.join(samtools_output, d + '.sam')
                    print("Converting %s to %s" % (sam_file, bam_file))
                    subprocess.call(["qsub", "-v", "out=%s,bam=%s" % (sam_file, bam_file), filename])

        # wait for all jobs to complete
        wait_for_job(jobname, sleep_time=1)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def run_htseq_count(self):
        """
        Based on the gff file and sam file counts the number of reads that map to a given gene
        """
        filename, jobname = self.write_submission_script("htseq_count_%d",
                                                         self.python_module,
                                                         self.htseq_count_cmd,
                                                         "htseq_count_%d.sh")

        for g in self.genomes:
            samtools_output = self.dp[g]['samtools_output']
            htseq_output = self.dp[g]['htseq_output']
            os.makedirs(htseq_output, exist_ok=True)

            gff_file = self.dp[g]['gff_file']
            gff_feature = self.dp[g]['gff_feature']
            gff_id = self.dp[g]['gff_id']

            sam_files = []

            for file in os.listdir(samtools_output):
                if file.endswith('.sam'):
                    sam_files.append(file)

            for sam_file in sam_files:
                sam_in = os.path.join(samtools_output, sam_file)
                htseq_out = os.path.join(htseq_output, sam_file.replace('.sam', '.htseq'))

                subprocess.call(["qsub", "-v", "feature=%s,field=%s,sam=%s,gff=%s,out=%s" % (gff_feature, gff_id, sam_in, gff_file, htseq_out), filename])

        # wait for all jobs to complete
        wait_for_job(jobname, sleep_time=1)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def htseq_to_matrix(self):
        """
        Groups all htseq files into one expression matrix

        """
        for g in self.genomes:
            htseq_output = self.dp[g]['htseq_output']
            os.makedirs(os.path.dirname(htseq_output), exist_ok=True)

            htseq_files = [f for f in os.listdir(htseq_output) if f.endswith('.htseq')]
            counts = {}

            for file in htseq_files:
                full_path = os.path.join(htseq_output, file)

                with open(full_path, "r") as f:
                    for row in f:
                        gene_id, count = row.strip().split('\t')

                        if gene_id not in counts.keys():
                            counts[gene_id] = {}

                        counts[gene_id][file] = count

            output_file = self.dp[g]['exp_matrix_output']
            with open(output_file, "w") as f_out:

                header = '\t'.join(htseq_files)
                print('gene\t' + header, file=f_out)

                bad_fields = ['no_feature', 'ambiguous', 'too_low_aQual', 'not_aligned', 'alignment_not_unique']
                for gene_id in counts:
                    values = []
                    for f in htseq_files:
                        if f in counts[gene_id].keys():
                            values.append(counts[gene_id][f])
                        else:
                            values.append('0')
                    if all([x not in gene_id for x in bad_fields]):
                        print(gene_id + '\t' + '\t'.join(values), file=f_out)

            print("Done\n\n")

    def normalize_rpkm(self):
        for g in self.genomes:
            data, conditions = read_matrix(self.dp[g]['exp_matrix_output'])
            normalized_data = normalize_matrix_counts(data, conditions)
            length_normalized_data = normalize_matrix_length(normalized_data, self.dp[g]['cds_fasta'])
            write_matrix(self.dp[g]['exp_matrix_rpkm_output'], conditions, length_normalized_data)

    def normalize_tpm(self):
        for g in self.genomes:
            data, conditions = read_matrix(self.dp[g]['exp_matrix_output'])
            length_normalized_data = normalize_matrix_length(data, self.dp[g]['cds_fasta'])
            normalized_data = normalize_matrix_counts(length_normalized_data, conditions)
            write_matrix(self.dp[g]['exp_matrix_tpm_output'], conditions, normalized_data)









