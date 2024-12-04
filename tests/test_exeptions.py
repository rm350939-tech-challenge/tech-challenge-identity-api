import pytest
from domain.exceptions import (
    CustomerAlreadyExistsException,
    CustomerNotFoundException,
    EntityNotFoundException,
    EntityAlreadyExistsException,
)


def test_customer_already_exists_exception():
    with pytest.raises(
        CustomerAlreadyExistsException, match="Customer already exists."
    ):
        raise CustomerAlreadyExistsException()

    custom_message = "Custom message: Customer already exists."
    with pytest.raises(CustomerAlreadyExistsException, match=custom_message):
        raise CustomerAlreadyExistsException(message=custom_message)


def test_customer_not_found_exception():
    with pytest.raises(CustomerNotFoundException, match="Customer not found."):
        raise CustomerNotFoundException()

    custom_message = "Custom message: Customer not found."
    with pytest.raises(CustomerNotFoundException, match=custom_message):
        raise CustomerNotFoundException(message=custom_message)


def test_entity_not_found_exception():
    custom_message = "Entity with ID 123 not found."
    with pytest.raises(EntityNotFoundException, match=custom_message):
        raise EntityNotFoundException(custom_message)


def test_entity_already_exists_exception():
    custom_message = "Entity with ID 123 already exists."
    with pytest.raises(EntityAlreadyExistsException, match=custom_message):
        raise EntityAlreadyExistsException(custom_message)
