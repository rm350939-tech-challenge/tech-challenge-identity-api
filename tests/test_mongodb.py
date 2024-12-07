import pytest
from unittest.mock import MagicMock
from pymongo.collection import Collection
from bson import ObjectId
from domain.entities import CustomerEntity, RegistrationStatus
from adapters.mongodb import CustomerMongodbRepository


@pytest.fixture
def mock_collection(mocker):
    """Mock da coleção MongoDB."""
    mock_collection = mocker.patch("adapters.mongodb.collection", autospec=True)
    return mock_collection


@pytest.fixture
def repository(mock_collection):
    """Instância do repositório com a coleção mockada."""
    return CustomerMongodbRepository()


@pytest.fixture
def mock_customer_entity():
    """Entidade de cliente fictícia para testes."""
    return CustomerEntity(
        id=None,
        name="John Doe",
        email="john.doe@example.com",
        national_id="123456789",
        registration_status=RegistrationStatus.COMPLETED,
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-02T00:00:00Z",
    )


def test_list_customers(repository, mock_collection):
    """Teste para listar clientes."""
    mock_collection.find.return_value = [
        {
            "_id": ObjectId("64a123456789abcdef123456"),
            "name": "John Doe",
            "email": "john.doe@example.com",
            "national_id": "123456789",
            "registration_status": RegistrationStatus.COMPLETED.value,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
        }
    ]

    customers = repository.list()

    assert len(customers) == 1
    assert customers[0].id == "64a123456789abcdef123456"
    assert customers[0].name == "John Doe"
    mock_collection.find.assert_called_once_with({})


def test_list_customers_empty(repository, mock_collection):
    """Teste para listar clientes quando não há registros."""
    mock_collection.find.return_value = []

    customers = repository.list()

    assert customers is None
    mock_collection.find.assert_called_once_with({})


def test_find_customer_by_national_id(repository, mock_collection):
    """Teste para buscar cliente pelo CPF."""
    mock_collection.find_one.return_value = {
        "_id": ObjectId("64a123456789abcdef123456"),
        "name": "John Doe",
        "email": "john.doe@example.com",
        "national_id": "123456789",
        "registration_status": RegistrationStatus.COMPLETED,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
    }

    customer = repository.find_customer_by_national_id("123456789")

    assert customer["id"] == "64a123456789abcdef123456"
    assert customer["name"] == "John Doe"
    mock_collection.find_one.assert_called_once_with({"national_id": "123456789"})


def test_find_customer_by_national_id_not_found(repository, mock_collection):
    """Teste para buscar cliente pelo CPF quando não encontrado."""
    mock_collection.find_one.return_value = None

    customer = repository.find_customer_by_national_id("987654321")

    assert customer is None
    mock_collection.find_one.assert_called_once_with({"national_id": "987654321"})
