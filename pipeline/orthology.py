import os
import subprocess
import sys
from shutil import copy

from cluster import wait_for_job

from .base import PipelineBase


class OrthologyPipeline(PipelineBase):

    def run_orthofinder(self):
        """
        Runs orthofinder for all genomes
        """
        orthofinder_dir = self.dp['GLOBAL']['orthofinder_output']
        orthofinder_cores = self.cp['TOOLS']['orthofinder_cores']

        os.makedirs(orthofinder_dir, exist_ok=True)

        filename, jobname = self.write_submission_script("orthofinder_%d",
                                                         self.python_module + ' ' +
                                                         self.blast_module + ' ' +
                                                         self.mcl_module,
                                                         self.orthofinder_cmd,
                                                         "orthofinder_%d.sh")

        for g in self.genomes:
            print('çopying', self.dp[g]['protein_fasta'], 'to', os.path.join(orthofinder_dir, g + '.fasta'))
            copy(self.dp[g]['protein_fasta'], os.path.join(orthofinder_dir, g + '.fasta'))

        subprocess.call(["qsub", "-pe", "cores", orthofinder_cores, "-v", "fasta_dir=" + orthofinder_dir + ",num_cores=" + orthofinder_cores, filename])

         # wait for all jobs to complete
        wait_for_job(jobname)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")

    def run_mcl(self):
        """
        Runs MCL clustering on OrthoFinder output to obtain homologous families (without re-running blast)
        """
        orthofinder_dir = self.dp['GLOBAL']['orthofinder_output']

        try:
            orthofinder_results_dir = list(filter(lambda x: 'Results_' in x, os.listdir(orthofinder_dir)))[0]
        except IndexError:
            print('No results found in orthofinder directory!', file=sys.stderr)
            quit()

        # Concatenate OrthoFinder blast files
        working_dir = os.path.join(orthofinder_dir, orthofinder_results_dir, 'WorkingDirectory')
        orthofinder_blast_files = list(filter(lambda x: x.startswith('Blast'), os.listdir(working_dir)))
        full_blast = os.path.join(working_dir, 'full_blast.out')
        full_blast_abc = os.path.join(working_dir, 'full_blast.abc')
        mcl_families_out = os.path.join(orthofinder_dir, 'mcl_families.unprocessed.txt')

        with open(full_blast, 'w') as outfile:
            for fname in orthofinder_blast_files:
                with open(os.path.join(working_dir, fname)) as infile:
                    for line in infile:
                        outfile.write(line)

        filename, jobname = self.write_submission_script("mcl_%d",
                                                         self.mcl_module,
                                                         self.mcxdeblast_cmd + '\n' +
                                                         self.mcl_cmd,
                                                         "mcl_%d.sh")
        # submit job
        subprocess.call(["qsub", "-pe", "cores", "4",
                         "-v", "blast_in=" + full_blast +
                         ",abc_out=" + full_blast_abc +
                         ",in=" + full_blast_abc +
                         ",out=" + mcl_families_out, filename])

        # wait for all jobs to complete
        wait_for_job(jobname)

        id_conversion = {}
        with open(os.path.join(working_dir, 'SequenceIDs.txt')) as infile:
            for line in infile:
                parts = line.strip().split()
                id = parts[0].strip(':')
                gene = parts[1]

                id_conversion[id] = gene

        with open(mcl_families_out, 'r') as infile, open(os.path.join(orthofinder_dir, 'mcl_families.processed.txt')) as outfile:
            for l in infile:
                parts = [id_conversion[id] if id in id_conversion.keys() else '!error!' for id in l.strip.split()]
                print('\t'.join(parts), outfile)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")
