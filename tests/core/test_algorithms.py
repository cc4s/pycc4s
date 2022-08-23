import pytest
from pydantic import ValidationError

from pycc4s.core.algorithms import (
    _ALGOS,
    AlgorithmInitializationError,
    AlgorithmInitializationWarning,
    BasisSetCorrectionAlgo,
    CoulombVertex,
    CoupledClusterAlgo,
    DefineHolesAndParticlesAlgo,
    EigenEnergies,
    FiniteSizeCorrectionAlgo,
    FName,
    PerturbativeTriplesAlgo,
    ReadAlgo,
    SecondOrderPerturbationTheoryAlgo,
    SlicedEigenEnergies,
    SliceOperatorAlgo,
    VertexCoulombIntegralsAlgo,
    WriteAlgo,
)


class TestAlgorithms:
    def test_algos(self):
        expected_names = {
            ReadAlgo: "Read",
            WriteAlgo: "Write",
            DefineHolesAndParticlesAlgo: "DefineHolesAndParticles",
            SliceOperatorAlgo: "SliceOperator",
            VertexCoulombIntegralsAlgo: "VertexCoulombIntegrals",
            CoupledClusterAlgo: "CoupledCluster",
            FiniteSizeCorrectionAlgo: "FiniteSizeCorrection",
            BasisSetCorrectionAlgo: "BasisSetCorrection",
            PerturbativeTriplesAlgo: "PerturbativeTriples",
            SecondOrderPerturbationTheoryAlgo: "SecondOrderPerturbationTheory",
        }
        expected_inputs = {
            ReadAlgo: ReadAlgo.Input,
            WriteAlgo: WriteAlgo.Input,
            DefineHolesAndParticlesAlgo: DefineHolesAndParticlesAlgo.Input,
            SliceOperatorAlgo: SliceOperatorAlgo.Input,
            VertexCoulombIntegralsAlgo: VertexCoulombIntegralsAlgo.Input,
            CoupledClusterAlgo: CoupledClusterAlgo.Input,
            FiniteSizeCorrectionAlgo: FiniteSizeCorrectionAlgo.Input,
            BasisSetCorrectionAlgo: BasisSetCorrectionAlgo.Input,
            PerturbativeTriplesAlgo: PerturbativeTriplesAlgo.Input,
            SecondOrderPerturbationTheoryAlgo: SecondOrderPerturbationTheoryAlgo.Input,
        }
        expected_outputs = {
            ReadAlgo: ReadAlgo.Output,
            WriteAlgo: WriteAlgo.Output,
            DefineHolesAndParticlesAlgo: DefineHolesAndParticlesAlgo.Output,
            SliceOperatorAlgo: SliceOperatorAlgo.Output,
            VertexCoulombIntegralsAlgo: VertexCoulombIntegralsAlgo.Output,
            CoupledClusterAlgo: CoupledClusterAlgo.Output,
            FiniteSizeCorrectionAlgo: FiniteSizeCorrectionAlgo.Output,
            BasisSetCorrectionAlgo: BasisSetCorrectionAlgo.Output,
            PerturbativeTriplesAlgo: PerturbativeTriplesAlgo.Output,
            SecondOrderPerturbationTheoryAlgo: SecondOrderPerturbationTheoryAlgo.Output,
        }
        for algo_name, algo_cls in _ALGOS.items():
            assert algo_cls.__fields__["name"].default == expected_names[algo_cls]
            assert algo_name == expected_names[algo_cls]
            assert algo_cls.Input == expected_inputs[algo_cls]
            assert algo_cls.Output == expected_outputs[algo_cls]

    def test_read_algo(self):
        algo = ReadAlgo(
            name="Read",
            input={"fileName": "CoulombVertex.yaml"},
            output={"destination": "tada"},
        )
        assert isinstance(algo.input, ReadAlgo.Input)
        assert isinstance(algo.output.destination, CoulombVertex)
        assert algo.output.destination.object_name() == "tada"
        with pytest.raises(AlgorithmInitializationError):
            ReadAlgo(
                input={"fileName": "CoulombVertex2.yaml"},
                output={"destination": "tada"},
            )
        algo = ReadAlgo(
            input={"fileName": "CoulombVertex2.yaml", "object_type": "CoulombVertex"},
            output={"destination": "tada"},
        )
        assert isinstance(algo.input, ReadAlgo.Input)
        assert isinstance(algo.output.destination, CoulombVertex)
        assert algo.output.destination.object_name() == "tada"
        assert algo.name == "Read"

        with pytest.warns(AlgorithmInitializationWarning):
            ReadAlgo(
                input={
                    "fileName": "CoulombVertex.yaml",
                    "object_type": "CoulombIntegrals",
                },
                output={"destination": "tada"},
            )

        with pytest.raises(ValidationError) as ve:
            ReadAlgo(
                name="somename",
                input={"fileName": "CoulombVertex.yaml"},
                output={"destination": "tada"},
            )
        errors = ve.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "value_error.const"
        assert errors[0]["ctx"] == {"given": "somename", "permitted": ["Read"]}

    def test_write_algo(self):
        algo = WriteAlgo(
            input={"source": "CV"},
            output={"fileName": "CoulombVertex.yaml"},
        )
        assert isinstance(algo.input, WriteAlgo.Input)
        assert isinstance(algo.input.source, str)
        assert isinstance(algo.output.fileName, FName)
        assert algo.name == "Write"

    def test_define_holes_and_particles_algo(self):
        algo = DefineHolesAndParticlesAlgo(
            input={"eigenEnergies": "EigenEnergies"},
            output={"slicedEigenEnergies": "EigenEnergies"},
        )
        assert isinstance(algo.input, DefineHolesAndParticlesAlgo.Input)
        assert isinstance(algo.input.eigenEnergies, EigenEnergies)
        assert isinstance(algo.output.slicedEigenEnergies, SlicedEigenEnergies)
        assert algo.name == "DefineHolesAndParticles"
