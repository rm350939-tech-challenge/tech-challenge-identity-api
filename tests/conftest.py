import pytest
from flask import Flask
from unittest.mock import MagicMock

@pytest.fixture
def mock_service(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("domain.services.CustomerService", mock)
    return mock
