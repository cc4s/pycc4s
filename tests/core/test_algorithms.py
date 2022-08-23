import pytest
from pydantic import ValidationError

from pycc4s.core.algorithms import (
    AlgorithmInitializationError,
    AlgorithmInitializationWarning,
    CoulombVertex,
    FName,
    ReadAlgo,
    WriteAlgo,
)


class TestAlgorithms:
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
            name="Write",
            input={"source": "CV"},
            output={"fileName": "CoulombVertex.yaml"},
        )
        assert isinstance(algo.input, WriteAlgo.Input)
        assert isinstance(algo.input.source, str)
        assert isinstance(algo.output.fileName, FName)
