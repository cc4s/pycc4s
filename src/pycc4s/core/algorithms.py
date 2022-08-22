"""Algorithms in CC4S."""
from importlib import import_module
from pathlib import Path
from typing import Optional

import yaml  # type: ignore
from monty.json import MSONable
from monty.serialization import dumpfn
from pydantic import BaseModel, validator
from pydantic.fields import ModelField


class BaseAlgo(MSONable, BaseModel):
    """Base class for CC4S algorithms."""

    name: str
    input: BaseModel
    output: BaseModel

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


class Object(str):
    """Class for objects used by the algorithms.

    Subclasses of this object are used to define the actual objects.
    These are then used to clarify inputs and outputs of the algorithms
    and how the algorithms can be sequenced.
    """

    def __str__(self):
        """Return a string representation of the Object."""
        return f'Object of type "{self.__class__.__name__}": {self.object_name()}'

    def object_name(self):
        """Return the name of the Object."""
        return super().__str__()

    def __eq__(self, other):
        """Test equality with respect to another Object."""
        return (
            self.__class__ == other.__class__
            and self.object_name() == other.object_name()
        )


class Amplitudes(Object):
    """Object class for Amplitudes."""


class CoulombIntegrals(Object):
    """Object class for Coulomb integrals."""


class CoulombPotential(Object):
    """Object class for Coulomb potential."""


class CoulombVertex(Object):
    """Object class for Coulomb vertex."""


class CoulombVertexSingularVectors(Object):
    """Object class for Coulomb vertex singular vectors."""


class DeltaIntegrals(Object):
    """Object class for Delta integrals."""


class EigenEnergies(Object):
    """Object class for eigen energies."""


class GridVectors(Object):
    """Object class for grid vectors."""


class Mp2PairEnergies(Object):
    """Object class for Mp2 pair energies."""


class SlicedCoulombVertex(Object):
    """Object class for sliced Coulomb vertex."""


class SlicedEigenEnergies(Object):
    """Object class for sliced eigen energies."""


# TODO: check here that structure factors are all the same objects
class StructureFactors(Object):
    """Object class for structure factors."""


class FName(str):
    """Class for filename.

    This is used to format the yaml input file as in the examples.
    Filenames in the algorithms are enclosed with double quotes while
    other str objects are not enclosed with doubles quotes.
    """


class InOutModel(BaseModel):
    """Base pydantic model for inputs and outputs."""

    @validator("*")
    def str_validation(cls, v, field):
        """Remove the double quotes if present and cast to the FName object."""
        if not isinstance(v, str):
            return v

        if field.type_ == FName:
            string = v.strip('"')
            if '"' in string:
                raise ValueError('Filename cannot contain double-quote (") character')
            return FName(string)
        elif issubclass(field.type_, Object):
            return field.type_(v)

        return v


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

    class Input(InOutModel):
        """Schema for input of Read algorithm."""

        fileName: FName
        object_type: Optional[str]

    class Output(InOutModel):
        """Schema for output of Read algorithm."""

        # Here we assume destination is a str
        destination: str

    @validator("output")
    def destination_object(cls, v, values):
        """Get the correct Object based on the filename."""
        fname = values["input"].fileName
        v.destination = get_object(fname, v.destination)
        return v


class WriteAlgo(BaseAlgo):
    """Write algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of Write algorithm."""

        # TODO: deal with filename based on source type here
        source: str

    class Output(InOutModel):
        """Schema for output of Write algorithm."""

        # TODO: deal with filename based on source type here
        fileName: FName


class DefineHolesAndParticlesAlgo(BaseAlgo):
    """DefineHolesAndParticles algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of DefineHolesAndParticles algorithm."""

        eigenEnergies: EigenEnergies

    class Output(InOutModel):
        """Schema for output of DefineHolesAndParticles algorithm."""

        slicedEigenEnergies: SlicedEigenEnergies


class SliceOperatorAlgo(BaseAlgo):
    """SliceOperator algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of SliceOperator algorithm."""

        slicedEigenEnergies: SlicedEigenEnergies
        # TODO: check here: is it always a CoulombVertex object ?
        operator: CoulombVertex

    class Output(InOutModel):
        """Schema for output of SliceOperator algorithm."""

        # TODO: check here: is it always a SlicedCoulombVertex object ?
        slicedOperator: SlicedCoulombVertex


class VertexCoulombIntegralsAlgo(BaseAlgo):
    """VertexCoulombIntegrals algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of VertexCoulombIntegrals algorithm."""

        slicedCoulombVertex: CoulombVertex

    class Output(InOutModel):
        """Schema for output of VertexCoulombIntegrals algorithm."""

        coulombIntegrals: CoulombIntegrals


class CoupledClusterAlgo(BaseAlgo):
    """CoupledCluster algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of CoupledCluster algorithm."""

        class MixerModel(BaseModel):
            """Schema for mixer parameters in amplitude equations solver."""

            type: str
            maxResidua: Optional[int]
            ratio: Optional[float]

        method: str
        linearized: Optional[int]
        integralsSliceSize: int
        slicedEigenEnergies: SlicedEigenEnergies
        coulombIntegrals: CoulombIntegrals
        slicedCoulombVertex: SlicedCoulombVertex
        maxIterations: int
        energyConvergence: str
        amplitudesConvergence: str
        mixer: MixerModel
        initialAmplitudes: Optional[Amplitudes]

    class Output(InOutModel):
        """Schema for output of CoupledCluster algorithm."""

        amplitudes: Amplitudes


class FiniteSizeCorrectionAlgo(BaseAlgo):
    """FiniteSizeCorrection algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of FiniteSizeCorrection algorithm."""

        amplitudes: Amplitudes
        coulombPotential: CoulombPotential
        slicedCoulombVertex: SlicedCoulombVertex
        coulombVertexSingularVectors: CoulombVertexSingularVectors
        gridVectors: GridVectors
        interpolationGridSize: Optional[int]

    class Output(InOutModel):
        """Schema for output of FiniteSizeCorrection algorithm."""

        transitionStructureFactor: StructureFactors


class BasisSetCorrectionAlgo(BaseAlgo):
    """BasisSetCorrection algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of BasisSetCorrection algorithm."""

        amplitudes: Amplitudes
        coulombIntegrals: CoulombIntegrals
        slicedEigenEnergies: SlicedEigenEnergies
        mp2PairEnergies: Mp2PairEnergies
        deltaIntegralsHH: DeltaIntegrals
        deltaIntegralsPPHH: DeltaIntegrals


class PerturbativeTriplesAlgo(BaseAlgo):
    """PerturbativeTriples algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of PerturbativeTriples algorithm."""

        amplitudes: Amplitudes
        coulombIntegrals: CoulombIntegrals
        slicedEigenEnergies: SlicedEigenEnergies
        mp2PairEnergies: Mp2PairEnergies


class SecondOrderPerturbationTheoryAlgo(BaseAlgo):
    """SecondOrderPerturbationTheory algorithm for CC4S."""

    class Input(InOutModel):
        """Schema for input of SecondOrderPerturbationTheory algorithm."""

        coulombIntegrals: CoulombIntegrals
        slicedEigenEnergies: SlicedEigenEnergies


_ALGOS = {
    "Read": ReadAlgo,
    "Write": WriteAlgo,
    "DefineHolesAndParticles": DefineHolesAndParticlesAlgo,
    "SliceOperator": SliceOperatorAlgo,
    "VertexCoulombIntegrals": VertexCoulombIntegralsAlgo,
    "CoupledCluster": CoupledClusterAlgo,
    "FiniteSizeCorrection": FiniteSizeCorrectionAlgo,
    "BasisSetCorrection": BasisSetCorrectionAlgo,
    "PerturbativeTriples": PerturbativeTriplesAlgo,
    "SecondOrderPerturbationTheory": SecondOrderPerturbationTheoryAlgo,
}


def get_algo(d):
    """Get algorithm from dictionary."""
    cls_ = _ALGOS[d["name"]]
    return cls_(name=d["name"], input=d["in"], output=d["out"])


_OBJECTS = {cls.__name__: cls for cls in Object.__subclasses__()}
_OBJECTS["DeltaIntegralsHH"] = DeltaIntegrals
_OBJECTS["DeltaIntegralsPPHH"] = DeltaIntegrals


def get_object(filename, destination):
    """Get object from string."""
    fpath = Path(filename)
    fpath = fpath.with_suffix("")
    cls_ = _OBJECTS[fpath.name]
    return cls_(destination)
