import pytest
from monty.tempfile import ScratchDir

from pycc4s.core.algorithms import (
    CoupledClusterAlgo,
    DefineHolesAndParticlesAlgo,
    ReadAlgo,
    SliceOperatorAlgo,
    VertexCoulombIntegralsAlgo,
    WriteAlgo,
)
from pycc4s.core.inputs import CC4SIn


class TestCC4SIn:
    def test_init(self):
        cc4sin = CC4SIn(
            algos=[
                ReadAlgo.from_filename("EigenEnergies.yaml"),
                DefineHolesAndParticlesAlgo.default(),
                WriteAlgo.from_object("SlicedEigenEnergies"),
            ]
        )
        cc4sin.validate()

    def test_from_file(self, test_data_dir):
        cc4sin = CC4SIn.from_file(test_data_dir / "cc4s.in")
        cc4sin.validate()
        assert len(cc4sin.algos) == 6
        assert isinstance(cc4sin.algos[0], ReadAlgo)
        assert isinstance(cc4sin.algos[1], ReadAlgo)
        assert isinstance(cc4sin.algos[2], DefineHolesAndParticlesAlgo)
        assert isinstance(cc4sin.algos[3], SliceOperatorAlgo)
        assert isinstance(cc4sin.algos[4], VertexCoulombIntegralsAlgo)
        assert isinstance(cc4sin.algos[5], CoupledClusterAlgo)
        cc4sin = CC4SIn.from_file(test_data_dir / "cc4s_invalid.in")
        with pytest.raises(ValueError):
            cc4sin.validate()

    def test_to_file(self):
        with ScratchDir("."):
            cc4sin = CC4SIn(
                algos=[
                    ReadAlgo.from_filename("EigenEnergies.yaml"),
                    DefineHolesAndParticlesAlgo.default(),
                    WriteAlgo.from_object("SlicedEigenEnergies"),
                ]
            )
            cc4sin.to_file()
            cc4sin2 = CC4SIn(
                algos=[
                    ReadAlgo.from_filename("EigenEnergies.yaml"),
                    DefineHolesAndParticlesAlgo.default(),
                    WriteAlgo.from_object("EigenEnergies"),
                ]
            )
            cc4sin_from_file = cc4sin.from_file()
            assert cc4sin_from_file == cc4sin
            assert cc4sin_from_file != cc4sin2
