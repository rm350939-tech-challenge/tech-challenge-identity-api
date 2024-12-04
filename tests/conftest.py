import pytest
from flask import Flask
from unittest.mock import MagicMock
from adapters.http import customer_api
from adapters.orm import CustomerModel


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(customer_api, url_prefix="/api/v1")
    app.config["TESTING"] = True
    return app


@pytest.fixture
def mock_service(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("domain.services.CustomerService", mock)
    return mock
