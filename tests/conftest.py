import pytest
from flask import Flask
from unittest.mock import MagicMock

from domain.services import CustomerService

@pytest.fixture
def mock_repository():
    """Mock do repositório CustomerMongodbRepository."""
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    """Instância de CustomerService com repositório mockado."""
    return CustomerService(customer_repository=mock_repository)

@pytest.fixture
def mock_service(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("domain.services.CustomerService", mock)
    return mock
