import pytest


@pytest.fixture(scope="session")
def test_data_dir():
    from pathlib import Path

    module_dir = Path(__file__).resolve().parent
    test_data_dir = module_dir / "test_data"
    return test_data_dir.resolve()
