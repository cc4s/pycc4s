"""Core module for cc4s flows."""


from dataclasses import dataclass, field

from atomate2.vasp.jobs.base import BaseVaspMaker
from atomate2.vasp.jobs.core import NonSCFMaker, StaticMaker
from jobflow import Flow, Maker

from pycc4s.workflows.jobs.base import BaseCC4SMaker
from pycc4s.workflows.jobs.core import CoupledClusterCC4SMaker
from pycc4s.workflows.sets.vasp import (
    NonSCFHFNOsSetGenerator,
    NonSCFHFSetGenerator,
    NonSCFMP2CBSSetGenerator,
    NonSCFMP2NOsSetGenerator,
    StaticHFSetGenerator,
    VaspDumpCc4sFilesGenerator,
)


@dataclass
class CoupledClusterMaker(Maker):
    """Maker for coupled cluster flow."""

    name: str = "Coupled Cluster"
    dft_static_maker: BaseVaspMaker = field(default_factory=StaticMaker)
    hf_static_maker: BaseVaspMaker = field(
        default=StaticMaker(input_set_generator=StaticHFSetGenerator())
    )
    hf_nonscf_maker: BaseVaspMaker = field(
        default=NonSCFMaker(input_set_generator=NonSCFHFSetGenerator())
    )
    mp2_cbs_maker: BaseVaspMaker = field(
        default=NonSCFMaker(input_set_generator=NonSCFMP2CBSSetGenerator())
    )
    mp2_nos_maker: BaseVaspMaker = field(
        default=NonSCFMaker(input_set_generator=NonSCFMP2NOsSetGenerator())
    )
    hf_nos_maker: BaseVaspMaker = field(
        default=NonSCFMaker(input_set_generator=NonSCFHFNOsSetGenerator())
    )
    cc4s_generation_maker: BaseVaspMaker = field(
        default=NonSCFMaker(input_set_generator=VaspDumpCc4sFilesGenerator())
    )
    coupled_cluster_cc4s_maker: BaseCC4SMaker = field(default=CoupledClusterCC4SMaker())

    def make(self, structure):
        """Return a coupled cluster flow."""
        dft_job = self.dft_static_maker.make(structure)
        hf_job = self.hf_static_maker.make(
            structure, prev_vasp_dir=dft_job.output.dir_name
        )
        hf_diag_job = self.hf_nonscf_maker.make(
            structure, prev_vasp_dir=hf_job.output.dir_name
        )
        mp2_cbs_job = self.mp2_cbs_maker.make(
            structure, prev_vasp_dir=hf_diag_job.output.dir_name
        )
        mp2_nos_job = self.mp2_nos_maker.make(
            structure, prev_vasp_dir=mp2_cbs_job.output.dir_name
        )
        hf_nos_job = self.hf_nos_maker.make(
            structure, prev_vasp_dir=mp2_nos_job.output.dir_name
        )
        cc4s_gen_job = self.cc4s_generation_maker.make(
            structure, prev_vasp_dir=hf_nos_job.output.dir_name
        )
        cc4s_job = self.coupled_cluster_cc4s_maker.make(
            structure, prev_dor=cc4s_gen_job.output.dir_name
        )
        return Flow(
            [
                dft_job,
                hf_job,
                hf_diag_job,
                mp2_cbs_job,
                mp2_nos_job,
                hf_nos_job,
                cc4s_gen_job,
                cc4s_job,
            ],
            output=cc4s_job.output,
        )
