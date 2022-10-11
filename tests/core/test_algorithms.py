from pathlib import Path

import pytest
from pydantic import ValidationError

from pycc4s.core.algorithms import (
    _ALGOS,
    AlgorithmInitializationError,
    AlgorithmInitializationWarning,
    Amplitudes,
    BasisSetCorrectionAlgo,
    CoulombIntegrals,
    CoulombPotential,
    CoulombVertex,
    CoulombVertexSingularVectors,
    CoupledClusterAlgo,
    DefineHolesAndParticlesAlgo,
    DeltaIntegrals,
    EigenEnergies,
    FiniteSizeCorrectionAlgo,
    FName,
    GridVectors,
    Mp2PairEnergies,
    PerturbativeTriplesAlgo,
    ReadAlgo,
    SecondOrderPerturbationTheoryAlgo,
    SlicedCoulombVertex,
    SlicedEigenEnergies,
    SliceOperatorAlgo,
    StructureFactors,
    VertexCoulombIntegralsAlgo,
    WriteAlgo,
)


class TestObjects:
    def test_eigenenergies(self):
        ee = EigenEnergies("EEObject")
        assert ee.object_name == "EEObject"
        assert ee.object_type == "EigenEnergies"
        assert ee.elements_files("in/Mybase") == {Path("in/Mybase.elements")}
        assert ee.additional_files("in/Mybase") == {Path("in/State.yaml")}

    def test_coulombvertex(self):
        ee = CoulombVertex("CV")
        assert ee.object_name == "CV"
        assert ee.object_type == "CoulombVertex"
        assert ee.elements_files("in/MyCV") == {Path("in/MyCV.elements")}
        assert ee.additional_files("in/MyCV") == {
            Path("in/State.yaml"),
            Path("in/AuxiliaryField.yaml"),
        }

    def test_slicedeigenenergies(self):
        ee = SlicedEigenEnergies("see")
        assert ee.object_name == "see"
        assert ee.object_type == "SlicedEigenEnergies"
        assert ee.elements_files("in/slicedee") == {
            Path("in/slicedee.components.h.elements"),
            Path("in/slicedee.components.p.elements"),
        }
        assert ee.additional_files("in/slicedee") == set()

    def test_slicedcoulombvertex(self):
        ee = SlicedCoulombVertex("scv")
        assert ee.object_name == "scv"
        assert ee.object_type == "SlicedCoulombVertex"
        assert ee.elements_files("in/slicedcv") == {
            Path("in/slicedcv.components.hh.elements"),
            Path("in/slicedcv.components.hp.elements"),
            Path("in/slicedcv.components.ph.elements"),
            Path("in/slicedcv.components.pp.elements"),
        }
        assert ee.additional_files("in/slicedcv") == set()

    def test_coulombintegrals(self):
        ee = CoulombIntegrals("CI")
        assert ee.object_name == "CI"
        assert ee.object_type == "CoulombIntegrals"
        assert ee.elements_files("in/ci") == {
            Path("in/ci.components.hhhh.elements"),
            Path("in/ci.components.hhhp.elements"),
            Path("in/ci.components.hhph.elements"),
            Path("in/ci.components.hphh.elements"),
            Path("in/ci.components.phhh.elements"),
            Path("in/ci.components.hhpp.elements"),
            Path("in/ci.components.hphp.elements"),
            Path("in/ci.components.hpph.elements"),
            Path("in/ci.components.phhp.elements"),
            Path("in/ci.components.phph.elements"),
            Path("in/ci.components.pphh.elements"),
            Path("in/ci.components.ppph.elements"),
            Path("in/ci.components.pphp.elements"),
            Path("in/ci.components.phpp.elements"),
            Path("in/ci.components.hppp.elements"),
            Path("in/ci.components.pppp.elements"),
        }
        assert ee.additional_files("in/ci") == set()

    def test_amplitudes(self):
        ee = Amplitudes("Amp")
        assert ee.object_name == "Amp"
        assert ee.object_type == "Amplitudes"
        assert ee.elements_files("in/amplit") == {
            Path("in/amplit.components.ph.elements"),
            Path("in/amplit.components.pphh.elements"),
        }
        assert ee.additional_files("in/amplit") == set()


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
        assert isinstance(algo.input.fileName, FName)
        assert isinstance(algo.output.destination, CoulombVertex)
        assert algo.output.destination.object_name == "tada"
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
        assert algo.output.destination.object_name == "tada"
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

        algo = ReadAlgo.from_filename("SlicedCoulombVertex.yaml")
        assert algo.input.fileName == "SlicedCoulombVertex.yaml"
        assert isinstance(algo.output.destination, SlicedCoulombVertex)
        assert algo.output.destination.object_name == "SlicedCoulombVertex"

    def test_write_algo(self):
        algo = WriteAlgo(
            input={"source": "CV", "fileName": "CoulombVertex.yaml"},
            output={},
        )
        assert isinstance(algo.input, WriteAlgo.Input)
        assert isinstance(algo.input.source, str)
        assert isinstance(algo.input.fileName, FName)
        assert algo.input.binary is None
        assert algo.name == "Write"

    def test_define_holes_and_particles_algo(self):
        algo = DefineHolesAndParticlesAlgo(
            input={"eigenEnergies": "EE"},
            output={"slicedEigenEnergies": "SEE"},
        )
        assert isinstance(algo.input, DefineHolesAndParticlesAlgo.Input)
        assert isinstance(algo.input.eigenEnergies, EigenEnergies)
        assert isinstance(algo.output.slicedEigenEnergies, SlicedEigenEnergies)
        assert algo.name == "DefineHolesAndParticles"
        algo = DefineHolesAndParticlesAlgo.default()
        assert algo.input.eigenEnergies.object_name == "EigenEnergies"

    def test_slice_operator_algo(self):
        algo = SliceOperatorAlgo(
            input={"slicedEigenEnergies": "EE", "operator": "CV"},
            output={"slicedOperator": "SCV"},
        )
        assert isinstance(algo.input.slicedEigenEnergies, SlicedEigenEnergies)
        assert algo.input.slicedEigenEnergies.object_name == "EE"
        assert isinstance(algo.input.operator, CoulombVertex)
        assert algo.input.operator.object_name == "CV"
        assert isinstance(algo.output.slicedOperator, SlicedCoulombVertex)
        assert algo.output.slicedOperator.object_name == "SCV"

    def test_vertex_coulomb_integrals_algo(self):
        algo = VertexCoulombIntegralsAlgo(
            input={"slicedCoulombVertex": "SCV"}, output={"coulombIntegrals": "CI"}
        )
        assert isinstance(algo.input.slicedCoulombVertex, SlicedCoulombVertex)
        assert algo.input.slicedCoulombVertex.object_name == "SCV"
        assert isinstance(algo.output.coulombIntegrals, CoulombIntegrals)
        assert algo.output.coulombIntegrals.object_name == "CI"

    def test_coupled_cluster_algo(self):
        algo = CoupledClusterAlgo(
            input={
                "method": "Ccsd",
                "integralsSliceSize": 100,
                "slicedEigenEnergies": "SEE",
                "coulombIntegrals": "CI",
                "slicedCoulombVertex": "SCV",
                "maxIterations": 30,
                "energyConvergence": 1.0e-8,
                "amplitudesConvergence": 1.0e-8,
                "mixer": {"type": "DiisMixer", "maxResidua": 4},
            },
            output={"amplitudes": "amp"},
        )
        assert isinstance(algo.input.slicedCoulombVertex, SlicedCoulombVertex)
        assert algo.input.slicedCoulombVertex.object_name == "SCV"
        assert isinstance(algo.input.slicedEigenEnergies, SlicedEigenEnergies)
        assert algo.input.slicedEigenEnergies.object_name == "SEE"
        assert isinstance(algo.input.coulombIntegrals, CoulombIntegrals)
        assert algo.input.coulombIntegrals.object_name == "CI"
        assert isinstance(algo.output.amplitudes, Amplitudes)
        assert algo.output.amplitudes.object_name == "amp"

    def test_finite_size_correction_algo(self):
        algo = FiniteSizeCorrectionAlgo(
            input={
                "amplitudes": "amp",
                "coulombPotential": "CP",
                "slicedCoulombVertex": "SCV",
                "coulombVertexSingularVectors": "CVSV",
                "gridVectors": "GV",
                "interpolationGridSize": 100,
            },
            output={"transitionStructureFactor": "TSF"},
        )

        assert isinstance(algo.input.amplitudes, Amplitudes)
        assert algo.input.amplitudes.object_name == "amp"
        assert isinstance(algo.input.coulombPotential, CoulombPotential)
        assert algo.input.coulombPotential.object_name == "CP"
        assert isinstance(algo.input.slicedCoulombVertex, SlicedCoulombVertex)
        assert algo.input.slicedCoulombVertex.object_name == "SCV"
        assert isinstance(
            algo.input.coulombVertexSingularVectors, CoulombVertexSingularVectors
        )
        assert algo.input.coulombVertexSingularVectors.object_name == "CVSV"
        assert isinstance(algo.input.gridVectors, GridVectors)
        assert algo.input.gridVectors.object_name == "GV"
        assert isinstance(algo.output.transitionStructureFactor, StructureFactors)
        assert algo.output.transitionStructureFactor.object_name == "TSF"

    def test_basis_set_correction_algo(self):
        algo = BasisSetCorrectionAlgo(
            input={
                "amplitudes": "amp",
                "coulombIntegrals": "CI",
                "slicedEigenEnergies": "SEE",
                "mp2PairEnergies": "MP2PE",
                "deltaIntegralsHH": "DIHH",
                "deltaIntegralsPPHH": "DIPPHH",
            },
            output={},
        )

        assert isinstance(algo.input.amplitudes, Amplitudes)
        assert algo.input.amplitudes.object_name == "amp"
        assert isinstance(algo.input.coulombIntegrals, CoulombIntegrals)
        assert algo.input.coulombIntegrals.object_name == "CI"
        assert isinstance(algo.input.slicedEigenEnergies, SlicedEigenEnergies)
        assert algo.input.slicedEigenEnergies.object_name == "SEE"
        assert isinstance(algo.input.mp2PairEnergies, Mp2PairEnergies)
        assert algo.input.mp2PairEnergies.object_name == "MP2PE"
        assert isinstance(algo.input.deltaIntegralsHH, DeltaIntegrals)
        assert algo.input.deltaIntegralsHH.object_name == "DIHH"
        assert isinstance(algo.input.deltaIntegralsPPHH, DeltaIntegrals)
        assert algo.input.deltaIntegralsPPHH.object_name == "DIPPHH"
        assert algo.output == {}

    def test_perturbative_triples_algo(self):
        algo = PerturbativeTriplesAlgo(
            input={
                "amplitudes": "amp",
                "coulombIntegrals": "CI",
                "slicedEigenEnergies": "SEE",
                "mp2PairEnergies": "MP2PE",
            },
            output={},
        )

        assert isinstance(algo.input.amplitudes, Amplitudes)
        assert algo.input.amplitudes.object_name == "amp"
        assert isinstance(algo.input.coulombIntegrals, CoulombIntegrals)
        assert algo.input.coulombIntegrals.object_name == "CI"
        assert isinstance(algo.input.slicedEigenEnergies, SlicedEigenEnergies)
        assert algo.input.slicedEigenEnergies.object_name == "SEE"
        assert isinstance(algo.input.mp2PairEnergies, Mp2PairEnergies)
        assert algo.input.mp2PairEnergies.object_name == "MP2PE"
        assert algo.output == {}

    def test_second_order_perturbation_theory_algo(self):
        algo = SecondOrderPerturbationTheoryAlgo(
            input={
                "coulombIntegrals": "CI",
                "slicedEigenEnergies": "SEE",
            },
            output={},
        )

        assert isinstance(algo.input.coulombIntegrals, CoulombIntegrals)
        assert algo.input.coulombIntegrals.object_name == "CI"
        assert isinstance(algo.input.slicedEigenEnergies, SlicedEigenEnergies)
        assert algo.input.slicedEigenEnergies.object_name == "SEE"
        assert algo.output == {}

    def test_algorithm_equality(self):
        algo1 = algo1bis = ReadAlgo(
            name="Read",
            input={"fileName": "CoulombVertex.yaml"},
            output={"destination": "tada"},
        )
        algo2 = ReadAlgo(
            name="Read",
            input={"fileName": "CoulombVertex.yaml"},
            output={"destination": "tada"},
        )
        algo3 = ReadAlgo(
            name="Read",
            input={"fileName": "CoulombVertex.yaml"},
            output={"destination": "tada2"},
        )
        assert algo1 == algo2
        assert algo1 != algo3
        assert algo1 is not algo2
        assert algo1 is algo1bis
