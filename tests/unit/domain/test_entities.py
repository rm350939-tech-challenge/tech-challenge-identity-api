from datetime import datetime

from domain.entities import CustomerEntity, RegistrationStatus
from domain.value_objects import Email, NationalID


class TestCustomer:

    def test_create_customer_with_all_data(self):
        name = "Luiz da Silva"
        email = Email("luiz.silva@teste.com")
        national_id = NationalID("000123")
        registration_status = RegistrationStatus.COMPLETED

        customer = CustomerEntity(name, email, national_id, registration_status)

        assert customer.name == name
        assert customer.email == email
        assert customer.national_id == national_id
        assert registration_status == RegistrationStatus.COMPLETED

    def test_method_as_dict(self):
        name = "Luiz da Silva"
        email = Email("luiz.silva@teste.com")
        national_id = NationalID("000123")
        registration_status = RegistrationStatus.COMPLETED

        customer = CustomerEntity(name, email, national_id, registration_status)

        assert customer.as_dict().get("name") == name
        assert customer.as_dict().get("email") == email.value
        assert customer.as_dict().get("national_id") == national_id.value
        assert customer.as_dict().get("registration_status") == registration_status.value

    def test_method_from_dict(self):
        data = {}
        data["id"] = 1
        data["name"] = "Luiz da Silva"
        data["email"] = "luiz.silva@teste.com"
        data["national_id"] = "000123"
        data["registration_status"] = 1
        data["created_at"] = "error test"
        customer = CustomerEntity.from_dict(data)
        assert isinstance(customer, CustomerEntity)

    def test_method_from_value_enum_registration_status(self):
        assert RegistrationStatus.COMPLETED == RegistrationStatus.from_value(2)
        assert RegistrationStatus.INCOMPLETE == RegistrationStatus.from_value(2)
        assert RegistrationStatus.PENDING == RegistrationStatus.from_value(3)

