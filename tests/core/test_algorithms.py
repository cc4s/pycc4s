from pycc4s.core.algorithms import CoulombVertex, ReadAlgo


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
