"""Base definition of input sets and generators for cc4s."""
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from atomate2.utils.file_client import auto_fileclient
from pymatgen.io.core import InputGenerator, InputSet

CC4SIN_FILENAME = "cc4s.in"


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
            copy_or_link(
                files=self.input_files,
                link_files=self.link_files,
            )

    @property
    def cc4sin(self):
        """Get the CC4SIn object."""
        return self[CC4SIN_FILENAME]


@auto_fileclient
def copy_or_link(
    files, src_host=None, dest_dir=None, file_client=None, link_files=True
):
    """Copy or link external input files to the cc4s directory."""
    dest_dir = dest_dir or "."
    dest_dir = file_client.abspath(dest_dir, host=None)

    for prev_file, input_file in files:
        src_file = file_client.abspath(prev_file, host=src_host)
        dest_file = Path(dest_dir, input_file)
        if link_files and src_host is None:
            file_client.link(src_file, dest_file)
        else:
            file_client.copy(src_file, dest_file, src_host=src_host)


@dataclass
class CC4SInputGenerator(InputGenerator):
    """A class to generate cc4s input sets."""

    calc_type: str = "cc4s_calculation"
