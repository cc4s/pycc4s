"""Core input set generators for cc4s."""
from dataclasses import dataclass

from pycc4s.core.algorithms import (
    CoupledClusterAlgo,
    DefineHolesAndParticlesAlgo,
    ReadAlgo,
    SliceOperatorAlgo,
    VertexCoulombIntegralsAlgo,
)
from pycc4s.core.inputs import CC4SIn
from pycc4s.workflows.sets.base import CC4SInputGenerator, CC4SInputSet


@dataclass
class CoupledClusterGenerator(CC4SInputGenerator):
    """Generator for coupled cluster calculations."""

    calc_type: str = "coupled_cluster"

    # TODO: add the parameters of the algorithms here (in particular of CoupledCluster)

    def get_input_set(self, eigen_energies_filepath, coulomb_vertex_filepath, **kwargs):
        """Get CC4SInputSet."""
        algos = []
        algos.append(ReadAlgo.from_filename("EigenEnergies.yaml"))
        algos.append(ReadAlgo.from_filename("CoulombVertex.yaml"))
        algos.append(DefineHolesAndParticlesAlgo.default())
        algos.append(SliceOperatorAlgo.default())
        algos.append(VertexCoulombIntegralsAlgo.default())
        algos.append(CoupledClusterAlgo.default())
        cc4sin = CC4SIn(algos=algos)
        input_files = {
            eigen_energies_filepath: "EigenEnergies.yaml",
            coulomb_vertex_filepath: "CoulombVertex.yaml",
        }
        cc4s_input_set = CC4SInputSet(
            cc4sin=cc4sin, input_files=input_files, link_files=True
        )
        return cc4s_input_set
