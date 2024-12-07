import pytest
from flask import Flask
from unittest.mock import MagicMock


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock das variáveis de ambiente para conexão com o MongoDB."""
    monkeypatch.setenv("DATABASE_MONGO_USER", "test_user")
    monkeypatch.setenv("DATABASE_MONGO_PASSWORD", "test_password")
    monkeypatch.setenv("DATABASE_MONGO_HOST", "test_host")
    monkeypatch.setenv("DATABASE_MONGO_DATABASE", "test_database")


@pytest.fixture
def mock_service(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("domain.services.CustomerService", mock)
    return mock
