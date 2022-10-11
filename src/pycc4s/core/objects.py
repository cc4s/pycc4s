"""Objects in CC4S."""
import warnings
from pathlib import Path
from typing import Optional, Tuple


class TensorObjectError(Exception):
    """Base exception for tensor objects."""


class TensorObjectInitializationError(TensorObjectError):
    """Exception raised when initialization of an object fails."""


class TensorObjectWarning(Warning):
    """Base warning for tensor objects."""


class TensorObjectInitializationWarning(Warning):
    """Base warning for initialization of a tensor object."""


class Object(str):
    """Class for objects used by the algorithms.

    Subclasses of this object are used to define the actual objects.
    These are then used to clarify inputs and outputs of the algorithms
    and how the algorithms can be sequenced. Information on their storage
    on file is also provided, e.g. extension of the file, extensions for the
    tensor components, additional files, ...
    """

    ext: str = ".yaml"
    elements_files_exts: Tuple[str, ...] = (".elements",)
    additional_filenames: Optional[Tuple] = None

    # def __str__(self):
    #     """Return a string representation of the Object."""
    #     return f'Object of type "{self.__class__.__name__}": {self.object_name()}'

    @property
    def object_name(self):
        """Return the name of the Object."""
        return super().__str__()

    @property
    def object_type(self):
        """Return the type of the Object."""
        return self.__class__.__name__

    def __eq__(self, other):
        """Test equality with respect to another Object."""
        return (
            self.__class__ == other.__class__ and self.object_name == other.object_name
        )

    @classmethod
    def elements_files(cls, basename):
        """Get the paths of the tensor components files (.elements files)."""
        if not cls.elements_files_exts:
            return set()
        if isinstance(basename, str):
            return set([Path(f"{basename}{ext}") for ext in cls.elements_files_exts])
        elif isinstance(basename, (tuple, list)):
            return set(
                [
                    tuple(Path(f"{bn}{ext}") for bn in basename)
                    for ext in cls.elements_files_exts
                ]
            )
        else:
            raise RuntimeError(
                "The basename should be a string or a tuple/list of strings."
            )

    @classmethod
    def additional_files(cls, basename):
        """Get the paths to the additional files."""
        if not cls.additional_filenames:
            return set()
        if isinstance(basename, str):
            basedir = Path(basename).parent
            return set([basedir / file for file in cls.additional_filenames])
        elif isinstance(basename, (tuple, list)):
            basedirs = [Path(bn).parent for bn in basename]
            return set(
                [
                    tuple(bd / file for bd in basedirs)
                    for file in cls.additional_filenames
                ]
            )


class Amplitudes(Object):
    """Object class for Amplitudes."""

    elements_files_exts = tuple(
        ".components.{}.elements".format(a) for a in ["ph", "pphh"]
    )


class CoulombIntegrals(Object):
    """Object class for Coulomb integrals."""

    elements_files_exts = tuple(
        ".components.{}{}{}{}.elements".format(a, b, c, d)
        for a in "hp"
        for b in "hp"
        for c in "hp"
        for d in "hp"
    )


class CoulombPotential(Object):
    """Object class for Coulomb potential."""

    additional_filenames = ("Momentum.yaml",)


class CoulombVertex(Object):
    """Object class for Coulomb vertex."""

    additional_filenames = (
        "State.yaml",
        "AuxiliaryField.yaml",
    )


class CoulombVertexSingularVectors(Object):
    """Object class for Coulomb vertex singular vectors."""

    additional_filenames = (
        "Momentum.yaml",
        "AuxiliaryField.yaml",
    )


class DeltaIntegrals(Object):
    """Object class for Delta integrals."""

    additional_filenames = ("State.yaml",)


class EigenEnergies(Object):
    """Object class for eigen energies."""

    additional_filenames = ("State.yaml",)


class GridVectors(Object):
    """Object class for grid vectors."""

    additional_filenames = ("Momentum.yaml",)


class Mp2PairEnergies(Object):
    """Object class for Mp2 pair energies."""

    additional_filenames = ("State.yaml",)


class SlicedCoulombVertex(Object):
    """Object class for sliced Coulomb vertex."""

    elements_files_exts = tuple(
        ".components.{}{}.elements".format(a, b) for a in "hp" for b in "hp"
    )


class SlicedEigenEnergies(Object):
    """Object class for sliced eigen energies."""

    elements_files_exts = tuple(".components.{}.elements".format(a) for a in "hp")


class StructureFactors(Object):
    """Object class for structure factors."""


class ResultDict(Object):
    """Object class for results."""

    elements_files_exts = None


class FName(str):
    """Class for filename.

    This is used to format the yaml input file as in the examples.
    Filenames in the algorithms are enclosed with double quotes while
    other str objects are not enclosed with doubles quotes.
    """


_OBJECTS = {cls.__name__: cls for cls in Object.__subclasses__()}
_OBJECTS["DeltaIntegralsHH"] = DeltaIntegrals
_OBJECTS["DeltaIntegralsPPHH"] = DeltaIntegrals


def get_object_cls(filename_or_string):
    """Get object class from filename or string."""
    fpath = Path(filename_or_string)
    fpath = fpath.with_suffix("")
    cls_ = _OBJECTS.get(fpath.name, None)
    return cls_


def get_object(filename_or_string, destination, object_type=None):
    """Get object from filename or string or a given type of Object."""
    cls_ = _OBJECTS.get(object_type, None)
    fpath = Path(filename_or_string)
    fpath = fpath.with_suffix("")
    cls_from_fpath = _OBJECTS.get(fpath.name, None)
    if cls_ is None:
        if cls_from_fpath is None:
            raise TensorObjectInitializationError("Cannot figure out type of Object.")
        cls_ = cls_from_fpath
    else:
        if cls_from_fpath is not None:
            if cls_ != cls_from_fpath:
                warnings.warn(
                    "Type of Object from filename does not match provided type.",
                    TensorObjectInitializationWarning,
                )
    return cls_(destination)
