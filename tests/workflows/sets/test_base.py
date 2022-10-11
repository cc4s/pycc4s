from pathlib import Path

import pytest
from monty.tempfile import ScratchDir

from pycc4s.core.objects import CoulombVertex
from pycc4s.workflows.sets.base import _object_dir_basename, copy_or_link_objects


def test_object_dir_basename():
    dirpath, basename = _object_dir_basename("a/b/c")
    assert dirpath == Path("a/b")
    assert basename == "c"
    dirpath, basename = _object_dir_basename("a/b/c.yaml")
    assert dirpath == Path("a/b")
    assert basename == "c"
    dirpath, basename = _object_dir_basename("a/b/c.elements")
    assert dirpath == Path("a/b")
    assert basename == "c"
    with pytest.raises(ValueError, match=r'File path cannot end with "\."\.'):
        _object_dir_basename("a/b/c.")
    with pytest.raises(ValueError, match=r"File path should have only one suffix\."):
        _object_dir_basename("a/b/c.yaml.tar.gz")
    with pytest.raises(
        ValueError, match=r'File path should have a "\.yaml" or "\.elements" suffix\.'
    ):
        _object_dir_basename("a/b/c.yml")


def test_copy_or_link_objects():
    with ScratchDir(".") as tmp:
        Path("prevdir").mkdir()
        Path("prevdir", "CoulombVertex.yaml").touch()
        Path("prevdir", "CoulombVertex.elements").touch()
        Path("indir").mkdir()
        copy_or_link_objects(
            {CoulombVertex: ("prevdir/SomeCoulombVertex.yaml", "CoulombVertex")},
            dest_dir="indir",
        )
        assert Path("indir", "CoulombVertex.yaml").is_symlink()
        assert Path("indir", "CoulombVertex.elements").is_symlink()
        assert Path("indir", "CoulombVertex.yaml").resolve() == Path(
            tmp, "prevdir", "SomeCoulombVertex.yaml"
        )
        assert Path("indir", "CoulombVertex.elements").resolve() == Path(
            tmp, "prevdir", "SomeCoulombVertex.elements"
        )
