import os

from .base import PipelineBase


class OrthologyPipeline(PipelineBase):

    def run_orthofinder(self):
        """
        Runs orthofinder for all genomes
        """
        orthofinder_dir = self.dp['GLOBAL']['orthofinder_output']
        os.makedirs(os.path.dirname(orthofinder_dir), exist_ok=True)

        for g in self.genomes:
            pass
