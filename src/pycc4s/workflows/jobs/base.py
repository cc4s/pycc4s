"""Core module for cc4s jobs."""
from dataclasses import dataclass
from typing import Optional

from jobflow import Maker

from pycc4s.workflows.sets.base import CC4SInputGenerator


@dataclass
class BaseCC4SMaker(Maker):
    """Maker for cc4s jobs."""

    input_set_generator: CC4SInputGenerator
    name: Optional[str] = None

    def __post_init__(self):
        """Process post-init configuration."""
        if self.name is None:
            self.name = self.input_set_generator.calc_type
