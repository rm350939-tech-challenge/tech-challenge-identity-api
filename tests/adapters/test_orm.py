import pytest
from unittest import mock
from datetime import datetime
from domain.entities import CustomerEntity, RegistrationStatus
from adapters.orm import CustomerRepository, CustomerModel
from domain.value_objects import Email, NationalID


@pytest.fixture
def mock_customer_data():
    return {
        "name": "John Doe",
        "email": Email("johndoe@example.com"),
        "national_id": NationalID("12345678901"),
        "registration_status": RegistrationStatus.COMPLETED,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


@pytest.fixture
def customer_entity(mock_customer_data):
    return CustomerEntity(**mock_customer_data)


@pytest.fixture
def repository():
    return CustomerRepository()


def test_create_customer(repository, customer_entity, mock_customer_data):
    with mock.patch.object(CustomerModel, 'save', return_value=None) as mock_save:
        # Mockando o comportamento de salvar
        mock_save.return_value = None
        customer = repository.create(customer_entity)
        
        # Verificando se o método save foi chamado
        mock_save.assert_called_once()
        
        # Verificando se o cliente retornado tem os dados corretos
        assert customer.name == mock_customer_data["name"]
        assert customer.email == mock_customer_data["email"].value
        assert customer.national_id == mock_customer_data["national_id"].value


def test_list_customers(repository, mock_customer_data):
    # Criando um mock do retorno de select
    mock_customer = mock.Mock()
    mock_customer.model_to_dict.return_value = mock_customer_data
    with mock.patch.object(CustomerModel, 'select', return_value=[mock_customer]):
        customers = repository.list()
        
        # Verificando se a lista de clientes não está vazia
        assert len(customers) == 1
        
        # Verificando se os dados estão corretos
        customer_dict = customers[0].as_dict()
        assert customer_dict['name'] == mock_customer_data['name']


def test_list_customers_empty(repository):
    # Testando quando não há clientes no banco
    with mock.patch.object(CustomerModel, 'select', return_value=[]):
        customers = repository.list()
        
        # Verificando se o retorno é None
        assert customers is None


def test_find_customer_by_national_id(repository, mock_customer_data):
    # Criando um mock para o método get_or_none
    mock_customer = mock.Mock()
    mock_customer.model_to_dict.return_value = mock_customer_data
    with mock.patch.object(CustomerModel, 'get_or_none', return_value=mock_customer):
        customer = repository.find_customer_by_national_id("12345678901")
        
        # Verificando se o método foi chamado corretamente
        customer_dict = customer
        assert customer_dict['name'] == mock_customer_data['name']
    
    # Caso o cliente não seja encontrado
    with mock.patch.object(CustomerModel, 'get_or_none', return_value=None):
        customer = repository.find_customer_by_national_id("99999999999")
        assert customer is None


def test_get_by_id(repository, mock_customer_data):
    # Criando um mock para o método get_or_none
    mock_customer = mock.Mock()
    mock_customer.model_to_dict.return_value = mock_customer_data
    with mock.patch.object(CustomerModel, 'get_or_none', return_value=mock_customer):
        customer = repository.get_by_id(1)
        
        # Verificando se o cliente foi retornado com os dados corretos
        assert customer.name == mock_customer_data["name"]
        assert customer.email == mock_customer_data["email"]
    
    # Caso o cliente não seja encontrado
    with mock.patch.object(CustomerModel, 'get_or_none', return_value=None):
        customer = repository.get_by_id(999)
        assert customer is None
