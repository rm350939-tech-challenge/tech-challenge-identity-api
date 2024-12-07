import pytest
from unittest.mock import MagicMock
from domain.entities import CustomerEntity, RegistrationStatus
from domain.exceptions import (
    CustomerAlreadyExistsException,
    CustomerNotFoundException,
    EntityNotFoundException,
)
from domain.value_objects import Email, NationalID
from domain.services import CustomerService


def test_identify_customer_by_national_id():
    mock_repository = MagicMock()
    customer_service = CustomerService(customer_repository=mock_repository)

    national_id_value = "123456789"
    mock_customer_data = {
        "id": "1234",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "national_id": national_id_value,
        "registration_status": RegistrationStatus.COMPLETED.value,
    }
    mock_repository.find_customer_by_national_id.return_value = mock_customer_data

    result = customer_service.identify_customer_by_national_id(national_id_value)
    assert isinstance(result, str)
    mock_repository.find_customer_by_national_id.assert_called_once_with(
        national_id=national_id_value
    )

    mock_repository.find_customer_by_national_id.return_value = None
    with pytest.raises(CustomerNotFoundException):
        customer_service.identify_customer_by_national_id(national_id_value)


def test_list_all_customers():
    mock_repository = MagicMock()
    customer_service = CustomerService(customer_repository=mock_repository)

    mock_customer_list = [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "national_id": "123456789",
            "registration_status": RegistrationStatus.COMPLETED.value,
        },
        {
            "id": 2,
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "national_id": "987654321",
            "registration_status": RegistrationStatus.INCOMPLETE.value,
        },
    ]
    mock_repository.list.return_value = mock_customer_list

    result = customer_service.list_all_customers()

    assert isinstance(result, list)
    assert len(result) == 2
    mock_repository.list.assert_called_once()

    mock_repository.list.return_value = []
    with pytest.raises(EntityNotFoundException):
        customer_service.list_all_customers()


def test_register_customer():
    mock_repository = MagicMock()
    customer_service = CustomerService(customer_repository=mock_repository)

    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "national_id": "123456789",
    }

    mock_customer_data = CustomerEntity(
        name="John Doe",
        email=Email("john.doe@example.com"),
        national_id=NationalID("123456789"),
        registration_status=RegistrationStatus.COMPLETED,
    )
    mock_repository.create.return_value = mock_customer_data
    mock_repository.find_customer_by_national_id.return_value = None

    result = customer_service.register_customer(**data)

    assert isinstance(result, CustomerEntity)
    assert result.name == "John Doe"
    assert result.email.value == "john.doe@example.com"
    assert result.registration_status == RegistrationStatus.COMPLETED

    mock_repository.find_customer_by_national_id.return_value = mock_customer_data
    with pytest.raises(CustomerAlreadyExistsException):
        customer_service.register_customer(**data)


def test_validate_already_exists():
    mock_repository = MagicMock()
    customer_service = CustomerService(customer_repository=mock_repository)

    national_id = "123456789"

    mock_repository.find_customer_by_national_id.return_value = {
        "id": 1,
        "name": "John Doe",
    }

    with pytest.raises(CustomerAlreadyExistsException):
        customer_service._validate_already_exists(national_id)

    mock_repository.find_customer_by_national_id.return_value = None
    result = customer_service._validate_already_exists(national_id)
    assert result is True
