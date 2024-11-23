from typing import Dict, List, Optional

from domain.entities import CustomerEntity, RegistrationStatus
from domain.exceptions import (
    CustomerAlreadyExistsException,
    CustomerNotFoundException,
    EntityNotFoundException,
)
from domain.value_objects import Email, NationalID

from ports.repositories import CustomerRepositoryInterface


class CustomerService:

    def __init__(self, customer_repository: CustomerRepositoryInterface):
        self._customer_repository = customer_repository

    def identify_customer_by_national_id(self, national_id: str) -> CustomerEntity:
        result = self._customer_repository.find_customer_by_national_id(
            national_id=NationalID(national_id).value
        )

        if not result:
            raise CustomerNotFoundException()

        return CustomerEntity.from_dict(result)

    def list_all_customers(self) -> List[CustomerEntity]:
        categories = self._customer_repository.list()

        if not categories:
            raise EntityNotFoundException("There are no registered customers.")

        return categories

    def register_customer(self, **data) -> CustomerEntity:
        email = Email(data.get("email"))
        national_id = NationalID(data.get("national_id"))
        name = data.get("name")

        self._validate_already_exists(national_id=national_id.value)

        registration_status = RegistrationStatus.INCOMPLETE
        if email.value.strip() and name.strip():
            registration_status = RegistrationStatus.COMPLETED

        customer = CustomerEntity(
            name=name,
            national_id=national_id,
            email=email,
            registration_status=registration_status,
        )

        customer_data_provider = self._customer_repository.create(customer)
        customer.id = customer_data_provider.id

        return customer

    def _validate_already_exists(
        self, national_id: str
    ) -> CustomerAlreadyExistsException | bool:
        customer = self._customer_repository.find_customer_by_national_id(
            national_id=national_id
        )
        if customer:
            raise CustomerAlreadyExistsException()
        return True
