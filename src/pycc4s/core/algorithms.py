"""Algorithms in CC4S."""
from importlib import import_module

import yaml  # type: ignore
from monty.json import MSONable
from monty.serialization import dumpfn
from pydantic import BaseModel, validator
from pydantic.fields import ModelField


class BaseAlgo(MSONable, BaseModel):
    """Base class for CC4S algorithms."""

    name: str
    input: dict
    output: dict

    def __init_subclass__(cls, *args, **kwargs):
        """Modify fields for algorithm subclass.

        This method is called when a new CC4S algorithm subclass is defined.

        We allow optional pydantic validation of the input and output provided.
        For this to work, one needs to define an inner Input class and an inner
        Output class in the subclass. These two Input and Output classes must
        inherit from pydantic's BaseModel.
        """
        if hasattr(cls, "Input"):
            prev_input_field = cls.__fields__["input"]
            input_field = ModelField(
                name=prev_input_field.name,
                type_=cls.Input,
                class_validators=prev_input_field.class_validators,
                model_config=prev_input_field.model_config,
                default=prev_input_field.default,
                default_factory=prev_input_field.default_factory,
                required=prev_input_field.required,
                alias=prev_input_field.alias,
                field_info=prev_input_field.field_info,
            )
            cls.__fields__["input"] = input_field
        if hasattr(cls, "Output"):
            prev_output_field = cls.__fields__["output"]
            output_field = ModelField(
                name=prev_output_field.name,
                type_=cls.Output,
                class_validators=prev_output_field.class_validators,
                model_config=prev_output_field.model_config,
                default=prev_output_field.default,
                default_factory=prev_output_field.default_factory,
                required=prev_output_field.required,
                alias=prev_output_field.alias,
                field_info=prev_output_field.field_info,
            )
            cls.__fields__["output"] = output_field
        super().__init_subclass__(*args, **kwargs)

    def dict(self, *args, **kwargs):
        """Override pydantic's dict method so that it handles correct names.

        The name for input is "in" in CC4S, which is a reserved word in python.
        Hence a mapping has been used here.
        """
        dd = super().dict(*args, **kwargs)
        dd["in"] = dd.pop("input")
        dd["out"] = dd.pop("output")
        return dd

    def as_dict(self):
        """Return a dict representation of the algorithm."""
        d = {"@module": self.__class__.__module__, "@class": self.__class__.__name__}

        try:
            parent_module = self.__class__.__module__.split(".", maxsplit=1)[0]
            module_version = import_module(parent_module).__version__  # type: ignore
            d["@version"] = str(module_version)
        except (AttributeError, ImportError):
            d["@version"] = None  # type: ignore

        d["name"] = self.name
        d["in"] = dict(self.input)
        d["out"] = dict(self.output)

        return d

    @classmethod
    def from_dict(cls, d):
        """Construct the algorithm from its dict representation."""
        return get_algo(d)

    @classmethod
    def from_file(cls, fname):
        """Construct the algorithm from file."""
        with open(fname, "r") as f:
            dd = yaml.safe_load(f)
            return get_algo(dd)

    def to_file(self, fname, format="yaml"):
        """Write algorithm to file."""
        if format == "yaml":
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
            dumpfn(d, fname)


class FName(str):
    """Class for filename.

    This is used to format the yaml input file as in the examples.
    Filenames in the algorithms are enclosed with double quotes while
    other str objects are not enclosed with doubles quotes.
    """


class FNameModel(BaseModel):
    """File name pydantic model."""

    fileName: FName

    @validator("fileName")
    def with_double_quotes(cls, v):
        """Remove the double quotes if present and cast to the FName object."""
        string = v.strip('"')
        if '"' in string:
            raise ValueError('Filename cannot contain double-quote (") character')
        return FName(string)


class MyDumper(yaml.Dumper):
    """Custom yaml dumper to represent filenames with double quotes.

    All the other fields will be represented with the default.
    """

    def represent_data(self, data):
        """Represent data in a customized way for CC4S algorithms.

        This will represent filenames (i.e. fields that are of type FName, which
        is a subclass of str) with double quotes surrounding the filename while
        other str will be represented as is.
        """
        if isinstance(data, FName):
            return self.represent_scalar("tag:yaml.org,2002:str", data, style='"')
        return super().represent_data(data)


class ReadAlgo(BaseAlgo):
    """Read algorithm for CC4S."""

    class Input(FNameModel):
        """Schema for input of Read algorithm."""

    class Output(BaseModel):
        """Schema for output of Read algorithm."""

        destination: str


class WriteAlgo(BaseAlgo):
    """Write algorithm for CC4S."""

    class Input(FNameModel):
        """Schema for input of Write algorithm."""

        source: str


class DefineHolesAndParticlesAlgo(BaseAlgo):
    """DefineHolesAndParticles algorithm for CC4S."""

    class Input(BaseModel):
        """Schema for input of DefineHolesAndParticles algorithm."""

        eigenEnergies: str

    class Output(BaseModel):
        """Schema for output of DefineHolesAndParticles algorithm."""

        slicedEigenEnergies: str


class SliceOperatorAlgo(BaseAlgo):
    """SliceOperator algorithm for CC4S."""

    class Input(BaseModel):
        """Schema for input of SliceOperator algorithm."""

        slicedEigenEnergies: str
        operator: str

    class Output(BaseModel):
        """Schema for output of SliceOperator algorithm."""

        slicedOperator: str


class VertexCoulombIntegralsAlgo(BaseAlgo):
    """VertexCoulombIntegrals algorithm for CC4S."""

    class Input(BaseModel):
        """Schema for input of VertexCoulombIntegrals algorithm."""

        slicedCoulombVertex: str

    class Output(BaseModel):
        """Schema for output of VertexCoulombIntegrals algorithm."""

        coulombIntegrals: str


class CoupledClusterAlgo(BaseAlgo):
    """CoupledCluster algorithm for CC4S."""

    class Input(BaseModel):
        """Schema for input of CoupledCluster algorithm."""

        class MixerModel(BaseModel):
            """Schema for mixer parameters in amplitude equations solver."""

            type: str
            maxResidua: int
            ratio: float

        method: str
        linearized: int
        integralsSliceSize: int
        slicedEigenEnergies: str
        coulombIntegrals: str
        slicedCoulombVertex: str
        maxIterations: int
        energyConvergence: str
        amplitudesConvergence: str
        mixer: MixerModel
        initialAmplitudes: str

    class Output(BaseModel):
        """Schema for output of CoupledCluster algorithm."""

        amplitudes: str


_ALGOS = {
    "Read": ReadAlgo,
    "Write": WriteAlgo,
    "DefineHolesAndParticles": DefineHolesAndParticlesAlgo,
    "SliceOperator": SliceOperatorAlgo,
    "VertexCoulombIntegrals": VertexCoulombIntegralsAlgo,
    "CoupledCluster": CoupledClusterAlgo,
}


def get_algo(d):
    """Get algorithm from dictionary."""
    cls_ = _ALGOS[d["name"]]
    return cls_(name=d["name"], input=d["in"], output=d["out"])
