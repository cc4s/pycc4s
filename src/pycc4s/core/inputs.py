"""Inputs for CC4S."""
from importlib import import_module
from typing import List

import yaml  # type: ignore
from monty.json import MSONable
from monty.serialization import dumpfn
from pydantic import BaseModel

from pycc4s.core.algorithms import BaseAlgo, MyDumper, get_algo


class CC4SIn(MSONable, BaseModel):
    """Class used to represent the input for CC4S."""

    algos: List[BaseAlgo]

    @classmethod
    def from_file(cls, fname):
        """Construct CC4SIn from file."""
        with open(fname, "r") as f:
            dd = yaml.safe_load(f)
            algos = [get_algo(algo_d) for algo_d in dd]
            return cls(algos=algos)

    def to_file(self, fname="cc4s.in", fmt=None):
        """Write CC4SIn to file."""
        if fmt is None and fname == "cc4s.in":
            fmt = "yaml"
        if fmt == "yaml":
            with open(fname, "w") as f:
                yaml.dump(
                    self.dict(),
                    f,
                    Dumper=MyDumper,
                    default_flow_style=False,
                    sort_keys=False,
                )
        else:
            d = self.as_dict()
            dumpfn(d, fname, fmt=fmt)

    def dict(self, *args, **kwargs):
        """Override pydantic's dict method so that it writes just the list of algos.

        The model contains an algos field but we don't want this field in the
        file that is written in the end. Indeed the CC4S input file is just a
        sequence of algorithms defined one after another.
        """
        dd = super().dict(*args, **kwargs)
        dd = dd["algos"]
        return dd

    def as_dict(self):
        """Return a dict representation of the CC4SIn object."""
        d = {"@module": self.__class__.__module__, "@class": self.__class__.__name__}

        try:
            parent_module = self.__class__.__module__.split(".", maxsplit=1)[0]
            module_version = import_module(parent_module).__version__  # type: ignore
            d["@version"] = str(module_version)
        except (AttributeError, ImportError):
            d["@version"] = None  # type: ignore

        d["algos"] = [algo.as_dict() for algo in self.algos]
        return d
