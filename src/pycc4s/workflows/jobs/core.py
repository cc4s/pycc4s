"""Core module for cc4s jobs."""
from dataclasses import dataclass

import yaml  # type: ignore
from jobflow import job

from pycc4s.custodian.jobs import OUTPUT_FILE_NAME
from pycc4s.workflows.jobs.base import BaseCC4SMaker
from pycc4s.workflows.run import run_cc4s
from pycc4s.workflows.sets.core import CoupledClusterGenerator


@dataclass
class CoupledClusterCC4SMaker(BaseCC4SMaker):
    """Maker for cc4s jobs."""

    input_set_generator: CoupledClusterGenerator = CoupledClusterGenerator()

    @job
    def make(self, eigen_energies_filepath, coulomb_vertex_filepath):
        """Return a cc4s jobflow.Job."""
        cc4s_input_set = self.input_set_generator.get_input_set(
            eigen_energies_filepath=eigen_energies_filepath,
            coulomb_vertex_filepath=coulomb_vertex_filepath,
        )
        cc4s_input_set.write_input(".")
        run_cc4s("mpirun -np 1 Cc4s")
        with open(OUTPUT_FILE_NAME, "r") as f:
            return yaml.safe_load(f)
