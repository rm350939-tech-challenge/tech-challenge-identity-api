import pytest
from datetime import datetime
from domain.value_objects import NationalID, Email
from domain.entities import CustomerEntity, RegistrationStatus


class Email:
    def __init__(self, value):
        self.value = value


class NationalID:
    def __init__(self, value):
        self.value = value


def test_registration_status_from_value():
    assert RegistrationStatus.from_value(1) == RegistrationStatus.COMPLETED
    assert RegistrationStatus.from_value(2) == RegistrationStatus.INCOMPLETE
    assert RegistrationStatus.from_value(3) == RegistrationStatus.PENDING


def test_customer_entity_as_dict():
    customer = CustomerEntity(
        id=1,
        name="John Doe",
        email=Email("john.doe@example.com"),
        national_id=NationalID("123456789"),
        registration_status=RegistrationStatus.COMPLETED,
    )

    result = customer.as_dict()

    assert isinstance(result, dict)
    assert result["name"] == "John Doe"
    assert result["email"] == "john.doe@example.com"
    assert result["national_id"] == "123456789"
    assert result["registration_status"] == 1
    assert "created_at" in result
    assert "updated_at" not in result


def test_customer_entity_from_dict():
    data = {
        "id": 1,
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "national_id": "987654321",
        "registration_status": 2,
        "created_at": datetime.now(),
        "updated_at": None,
    }

    customer = CustomerEntity.from_dict(data)

    assert isinstance(customer, CustomerEntity)
    assert customer.name == "Jane Doe"
    assert customer.email.value == "jane.doe@example.com"
    assert customer.national_id.value == "987654321"
    assert customer.registration_status == RegistrationStatus.INCOMPLETE
    assert customer.created_at is not None
    assert customer.updated_at is None


def test_customer_entity_from_dict_invalid_data():
    data = {
        "id": 1,
        "name": "Invalid User",
        "email": "invalid.email",
        "national_id": "invalid_nid",
        "registration_status": 99,
        "created_at": datetime.now(),
        "updated_at": None,
    }

    with pytest.raises(ValueError):
        CustomerEntity.from_dict(data)
