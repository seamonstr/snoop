import pytest
from unittest.mock import patch, Mock

from backend import logging

failing_tests = [
    # Fail cases, in various different orders
    ["stuff", "backend.stuff", "backend"],
    ["backend.stuff", "stuff", "backend"],
    ["stuff", "backend", "backend.stuff"],
]

passing_tests = [
    ["stuff", "more.stuff"],
    ["stuff", "backend"],
]


@pytest.mark.parametrize("modules", failing_tests)
@patch("backend.logging.modules")
@patch("backend.logging.fileConfig")
def test_configure_logging_failures(
    file_config_mock: Mock, modules_mock: Mock, modules: list[str]
):
    modules_mock.__iter__.return_value = modules
    with pytest.raises(RuntimeError, match=".*before logging.*"):
        logging.configure_logging("anything")
    file_config_mock.assert_not_called()


@pytest.mark.parametrize("modules", passing_tests)
@patch("backend.logging.modules")
@patch("backend.logging.fileConfig")
def test_configure_logging_passes(
    file_config_mock: Mock, modules_mock: Mock, modules: list[str]
):
    modules_mock.__iter__.return_value = modules
    TEST_CFG = "some_config.cfg"
    logging.configure_logging(TEST_CFG)
    file_config_mock.assert_called_with(TEST_CFG)
