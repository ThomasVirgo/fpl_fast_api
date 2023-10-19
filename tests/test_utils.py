from tests.factories.schema import overview_factory
from fpl.utils import requires_reload
import pytest


@pytest.mark.parametrize(
    "created_at_str, needs_reload",
    [
        ("2023-10-11T13:05:40.252833+00:00", False),
        ("2023-10-01T13:05:40.252833+00:00", True),
    ],
)
def test_requires_reload(created_at_str: str, needs_reload: bool):
    overview = overview_factory()
    assert requires_reload(overview, created_at_str) == needs_reload
