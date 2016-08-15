import subprocess
import os
import sys

from cluster import wait_for_job
from utils.matrix import read_matrix, write_matrix, normalize_matrix_counts, normalize_matrix_length
from .base import PipelineBase
from .check.quality import check_tophat, check_htseq


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

    def trim_fastq(self, overwrite=False):
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
                        if overwrite or not os.path.exists(outap):
                            print('Submitting pair %s, %s' % (file, pair_file))
                            subprocess.call(["qsub", "-v", "ina=%s,inb=%s,outap=%s,outau=%s,outbp=%s,outbu=%s" % (ina, inb, outap, outau, outbp, outbu), filename_pe])
                        else:
                            print('Found', outap, 'skipping')
                    else:
                        outfile = file.replace('.fq.gz', '.trimmed.fq.gz') if file.endswith('.fq.gz') else file.replace('.fastq.gz', '.trimmed.fastq.gz')
                        if overwrite or not os.path.exists(os.path.join(trimmed_output, outfile)):
                            print('Submitting single %s' % file)
                            subprocess.call(["qsub", "-v", "in=" + os.path.join(fastq_input_dir, file) + ",out=" + os.path.join(trimmed_output, outfile), filename_se])
                        else:
                            print('Found', outfile, 'skipping')
                else:
                    outfile = file.replace('.fq.gz', '.trimmed.fq.gz') if file.endswith('.fq.gz') else file.replace('.fastq.gz', '.trimmed.fastq.gz')
                    if overwrite or not os.path.exists(os.path.join(trimmed_output, outfile)):
                        print('Submitting single %s' % file)
                        subprocess.call(["qsub", "-v", "in=" + os.path.join(fastq_input_dir, file) + ",out=" + os.path.join(trimmed_output, outfile), filename_se])
                    else:
                        print('Found', outfile, 'skipping')

        print('Trimming fastq files...')

        # wait for all jobs to complete
        wait_for_job(jobname, sleep_time=1)

        # remove the submission script
        os.remove(filename_se)
        os.remove(filename_pe)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def run_tophat(self, overwrite=False, keep_previous=False):
        """
        Maps the reads from the trimmed fastq files to the bowtie-indexed genome

        :param overwrite: when true the pipeline will start tophat even if the output exists
        :param keep_previous: when true trimmed fastq files will not be removed after tophat completes
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
                    if overwrite or not os.path.exists(os.path.join(output_dir, 'accepted_hits.bam')):
                        print('Submitting pair %s, %s' % (pe_file, pair_file))
                        subprocess.call(["qsub", "-pe", "cores", "4", "-v", "out=%s,genome=%s,forward=%s,reverse=%s" % (output_dir, bowtie_output, forward, reverse), filename_pe])
                    else:
                        print('Output exists, skipping', pe_file)

            for se_file in se_files:
                output_dir = se_file.replace('.trimmed.fq.gz', '').replace('.trimmed.fastq.gz', '')
                output_dir = os.path.join(tophat_output, output_dir)
                if overwrite or not os.path.exists(os.path.join(output_dir, 'accepted_hits.bam')):
                    print('Submitting single %s' % se_file)
                    subprocess.call(["qsub", "-pe", "cores", "4", "-v", "out=%s,genome=%s,fq=%s" % (output_dir, bowtie_output, os.path.join(trimmed_fastq_dir, se_file)), filename_se])
                else:
                    print('Output exists, skipping', se_file)

        # wait for all jobs to complete
        wait_for_job(jobname, sleep_time=1)

        # remove all trimmed fastq files when keep_previous is disabled
        if not keep_previous:
            for g in self.genomes:
                trimmed_fastq_dir = self.dp[g]['trimmomatic_output']
                for file in os.listdir(trimmed_fastq_dir):
                    os.remove(os.path.join(trimmed_fastq_dir, file))

        # remove the submission script
        os.remove(filename_se)
        os.remove(filename_pe)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def run_htseq_count(self, keep_previous=False):
        """
        Based on the gff file and sam file counts the number of reads that map to a given gene

        :param keep_previous: when true sam files output will not be removed after htseq-count completes
        """
        filename, jobname = self.write_submission_script("htseq_count_%d",
                                                         (self.samtools_module + '\t' + self.python_module),
                                                         self.htseq_count_cmd,
                                                         "htseq_count_%d.sh")

        for g in self.genomes:
            tophat_output = self.dp[g]['tophat_output']
            htseq_output = self.dp[g]['htseq_output']
            os.makedirs(htseq_output, exist_ok=True)

            gff_file = self.dp[g]['gff_file']
            gff_feature = self.dp[g]['gff_feature']
            gff_id = self.dp[g]['gff_id']

            dirs = [o for o in os.listdir(tophat_output) if os.path.isdir(os.path.join(tophat_output, o))]
            bam_files = []
            for d in dirs:
                bam_file = os.path.join(tophat_output, d, 'accepted_hits.bam')
                if os.path.exists(bam_file):
                    bam_files.append((d, bam_file))

            for d, bam_file in bam_files:
                htseq_out = os.path.join(htseq_output, d + '.htseq')
                print(d, bam_file, htseq_out)

                subprocess.call(["qsub", "-v", "feature=%s,field=%s,bam=%s,gff=%s,out=%s" % (gff_feature, gff_id, bam_file, gff_file, htseq_out), filename])

        # wait for all jobs to complete
        wait_for_job(jobname, sleep_time=1)

        # remove all tophat files files when keep_previous is disabled
        # NOTE: only the large bam file is removed (for now)
        if not keep_previous:
            for g in self.genomes:
                tophat_output = self.dp[g]['tophat_output']
                dirs = [o for o in os.listdir(tophat_output) if os.path.isdir(os.path.join(tophat_output, o))]
                for d in dirs:
                    bam_file = os.path.join(tophat_output, d, 'accepted_hits.bam')
                    os.remove(bam_file)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def check_quality(self):
        print("Checking quality of samples based on TopHat mapping statistics")
        for g in self.genomes:
            tophat_output = self.dp[g]['tophat_output']
            htseq_output = self.dp[g]['htseq_output']

            dirs = [o for o in os.listdir(tophat_output) if os.path.isdir(os.path.join(tophat_output, o))]
            summary_files = []
            for d in dirs:
                summary_file = os.path.join(tophat_output, d, 'align_summary.txt')
                if os.path.exists(summary_file):
                    summary_files.append((d, summary_file))

            htseq_files = [os.path.join(htseq_output, f) for f in os.listdir(htseq_output) if f.endswith('.htseq')]

            for (d, s) in summary_files:
                cutoff = int(self.dp[g]['tophat_cutoff']) if 'tophat_cutoff' in self.dp[g] else 0
                passed = check_tophat(s, cutoff=cutoff, log=self.log)

                if not passed:
                    print('WARNING: sample with insufficient quality (TopHat) detected:', d, file=sys.stderr)
                    print('WARNING: check the log for additional information', file=sys.stderr)

            for h in htseq_files:
                cutoff = int(self.dp[g]['htseq_cutoff']) if 'htseq_cutoff' in self.dp[g] else 0
                passed = check_htseq(h, cutoff=cutoff, log=self.log)
                if not passed:
                    print('WARNING: sample with insufficient quality (HTSEQ-Count) detected:', d, file=sys.stderr)
                    print('WARNING: check the log for additional information', file=sys.stderr)

    def htseq_to_matrix(self):
        """
        Groups all htseq files into one expression matrix
        """
        for g in self.genomes:
            htseq_output = self.dp[g]['htseq_output']
            os.makedirs(os.path.dirname(htseq_output), exist_ok=True)

            # Check directory for .htseq files and apply quality control, keep valid files
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
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
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
        """
        Applies rpkm normalization to the htseq-counts expression matrix

        Note that as this is not a cpu intensive process it is done as part of the main pipeline
        """
        for g in self.genomes:
            data, conditions = read_matrix(self.dp[g]['exp_matrix_output'])
            normalized_data = normalize_matrix_counts(data, conditions)
            length_normalized_data = normalize_matrix_length(normalized_data, self.dp[g]['cds_fasta'])
            os.makedirs(os.path.dirname(self.dp[g]['exp_matrix_rpkm_output']), exist_ok=True)
            write_matrix(self.dp[g]['exp_matrix_rpkm_output'], conditions, length_normalized_data)

    def normalize_tpm(self):
        """
        Applies tpm normalization to the htseq-counts expression matrix

        Note that as this is not a cpu intensive process it is done as part of the main pipeline
        """
        for g in self.genomes:
            data, conditions = read_matrix(self.dp[g]['exp_matrix_output'])
            length_normalized_data = normalize_matrix_length(data, self.dp[g]['cds_fasta'])
            normalized_data = normalize_matrix_counts(length_normalized_data, conditions)
            os.makedirs(os.path.dirname(self.dp[g]['exp_matrix_rpkm_output']), exist_ok=True)
            write_matrix(self.dp[g]['exp_matrix_tpm_output'], conditions, normalized_data)

    def run_pcc(self, matrix_type='tpm'):
        """
        Calculates pcc values on the cluster using the pcc.py script included in RSTrAP.

        :param matrix_type: tpm or rpkm, select the desired matrix
        """
        filename, jobname = self.write_submission_script("pcc_wrapper_%d",
                                                         self.python3_module,
                                                         self.pcc_cmd,
                                                         "pcc_wrapper_%d.sh")

        for g in self.genomes:
            pcc_out = self.dp[g]['pcc_output']
            mcl_out = self.dp[g]['pcc_mcl_output']

            os.makedirs(os.path.dirname(self.dp[g]['pcc_output']), exist_ok=True)
            os.makedirs(os.path.dirname(self.dp[g]['pcc_mcl_output']), exist_ok=True)

            if matrix_type == 'tpm':
                htseq_matrix = self.dp[g]['exp_matrix_tpm_output']
            elif matrix_type == 'rpkm':
                htseq_matrix = self.dp[g]['exp_matrix_rpkm_output']
            else:
                print('Matrix type %s unknown, quiting...' % matrix_type)
                quit()

            subprocess.call(["qsub", "-v", "in=%s,out=%s,mcl_out=%s" % (htseq_matrix, pcc_out, mcl_out), filename])

        # wait for all jobs to complete
        wait_for_job(jobname, sleep_time=1)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def cluster_pcc(self):
        """
        Creates co-expression clusters using mcl.
        """
        filename, jobname = self.write_submission_script("cluster_pcc_%d",
                                                         self.mcl_module,
                                                         self.mcl_cmd,
                                                         "cluster_pcc_%d.sh")

        for g in self.genomes:
            # TODO naming convention here is confusing, improve this !
            mcl_out = self.dp[g]['pcc_mcl_output']
            mcl_clusters = self.dp[g]['mcl_cluster_output']

            subprocess.call(["qsub", "-pe", "cores", "4", "-v", "in=%s,out=%s" % (mcl_out, mcl_clusters), filename])

        # wait for all jobs to complete
        wait_for_job(jobname, sleep_time=1)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")


