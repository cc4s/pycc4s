"""Base definition of input sets and generators for cc4s."""
from dataclasses import dataclass
from pathlib import Path
from typing import Union

# TODO: change this when pull request in atomate2 has been merged
from atomate2.utils.file_client import FileClient as Atm2FileClient

# from atomate2.utils.file_client import auto_fileclient
from pymatgen.io.core import InputGenerator, InputSet

CC4SIN_FILENAME = "cc4s.in"


# TODO: remove this when pull request in atomate2 has been merged
class FileClient(Atm2FileClient):
    """Temporary FileClient (to be removed when pull request has been merged)."""

    def link(
        self,
        src_filename,
        dest_filename,
    ):
        """Link a file from source to destination.

        Parameters
        ----------
        src_filename : str or Path
            Full path to source file.
        dest_filename : str or Path
            Full path to destination file.
        """
        import errno
        import os

        try:
            os.symlink(src_filename, dest_filename)
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(dest_filename)
                os.symlink(src_filename, dest_filename)
            else:
                raise e


# TODO: remove this when pull request in atomate2 has been merged
def auto_fileclient(method=None):
    """Automatically pass FileClient to the function if not already present in kwargs.

    This decorator should only be applied to functions with a ``file_client`` keyword
    argument. If a custom file client is not supplied when the function is called, it
    will automatically create a new FileClient, add it to the function arguments and
    close the file client connects at the end of the function.

    Parameters
    ----------
    method : callable or None
        A function to wrap. This should not be specified directly and is implied
        by the decorator.
    """
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def gen_fileclient(*args, **kwargs):
            file_client = kwargs.get("file_client", None)
            if file_client is None:
                with FileClient() as file_client:
                    kwargs["file_client"] = file_client
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return gen_fileclient

    # See if we're being called as @auto_fileclient or @auto_fileclient().
    if method is None:
        # We're called with parens.
        return decorator

    # We're called as @auto_fileclient without parens.
    return decorator(method)


class CC4SInputSet(InputSet):
    """A class to represent a set of cc4s inputs."""

    def __init__(self, cc4sin, input_files=None, link_files=True):
        """Construct CC4SInputSet."""
        self.input_files = input_files
        self.link_files = link_files
        super().__init__(
            inputs={
                CC4SIN_FILENAME: cc4sin,
            }
        )

    def write_input(
        self,
        directory: Union[str, Path],
        make_dir: bool = True,
        overwrite: bool = True,
        zip_inputs: bool = False,
    ):
        """Write cc4s input files to a directory."""
        super().write_input(
            directory=directory,
            make_dir=make_dir,
            overwrite=overwrite,
            zip_inputs=zip_inputs,
        )

        if self.input_files:
            indir = Path(directory, "in")
            indir.mkdir()
            copy_or_link_objects(
                files=self.input_files,
                dest_dir=indir,
                link_files=self.link_files,
            )

    @property
    def cc4sin(self):
        """Get the CC4SIn object."""
        return self[CC4SIN_FILENAME]


def _object_dir_basename(fpath):
    """Get the directory and base name of a given object file path.

    The file path can be the yaml file, the elements file, or the base name,
    e.g. "CoulombVertex.yaml", "CoulombVertex.elements" or "CoulombVertex".
    """
    fpath = Path(fpath)
    if fpath.name.endswith("."):
        raise ValueError('File path cannot end with ".".')
    if fpath.with_suffix("") == fpath:
        return fpath.parent, fpath.stem
    suffixes = fpath.suffixes
    if len(suffixes) != 1:
        raise ValueError("File path should have only one suffix.")
    if suffixes[0] not in [".yaml", ".elements"]:
        raise ValueError('File path should have a ".yaml" or ".elements" suffix.')
    return fpath.parent, fpath.with_suffix("").stem


@auto_fileclient
def copy_or_link_objects(
    files, src_host=None, dest_dir=None, file_client=None, link_files=True
):
    """Copy or link external input files to the cc4s directory."""
    dest_dir = dest_dir or "."
    dest_dir = file_client.abspath(dest_dir, host=None)

    for prev_file, input_file in files.items():
        prev_dir, prev_base = _object_dir_basename(prev_file)
        input_dir, input_base = _object_dir_basename(input_file)
        if input_dir != Path("."):
            raise ValueError(
                "The input file should be a filename or a basename, not a path."
            )
        for suffix in [".yaml", ".elements"]:
            src_file = file_client.abspath(
                Path(prev_dir, prev_base).with_suffix(suffix), host=src_host
            )
            dest_file = Path(dest_dir, input_file).absolute().with_suffix(suffix)
            if link_files and src_host is None:
                file_client.link(src_file, dest_file)
            else:
                file_client.copy(src_file, dest_file, src_host=src_host)


@dataclass
class CC4SInputGenerator(InputGenerator):
    """A class to generate cc4s input sets."""

    calc_type: str = "cc4s_calculation"
