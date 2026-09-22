import pytest
from main import get_target_size, PRESETS


def test_get_target_size_with_valid_preset():
    assert get_target_size(preset="small") == PRESETS["small"]


def test_get_target_size_with_custom_dimensions():
    assert get_target_size(width=200, height=300) == (200, 300)


def test_get_target_size_with_invalid_preset():
    with pytest.raises(ValueError):
        get_target_size(preset="not_real")


def test_get_target_size_with_nothing_provided():
    with pytest.raises(ValueError):
        get_target_size()