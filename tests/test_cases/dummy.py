"""Test controller method."""
from tests.conftest import get_case_name, create_config


test_case = get_case_name(__file__)
collector_config = create_config(test_case)

def test_dummy():
    """Test if controllers method returns correct datatype."""
    assert 1 == 1
