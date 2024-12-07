from datetime import datetime
from domain.entities import CustomerEntity, RegistrationStatus
from domain.value_objects import Email, NationalID
from adapters.dto import OutputCustomerDTO


def test_from_domain():
    customer_entity = CustomerEntity(
        id="12345",
        name="John Doe",
        email=Email("john.doe@example.com"),
        national_id=NationalID("123456789"),
        registration_status=RegistrationStatus.COMPLETED,
        created_at=datetime(2024, 12, 2, 12, 30, 0),
        updated_at=None,
    )

    dto = OutputCustomerDTO.from_domain(customer_entity)

    assert dto.id == "12345"
    assert dto.name == "John Doe"
    assert dto.email == "john.doe@example.com"
    assert dto.national_id == "123456789"
    assert dto.registration_status == "COMPLETED"
    assert dto.created_at == "2024-12-02T12:30:00Z"
    assert dto.updated_at is None


def test_from_domain_with_updated_at():
    customer_entity = CustomerEntity(
        id="123455",
        name="Jane Doe",
        email=Email("jane.doe@example.com"),
        national_id=NationalID("987654321"),
        registration_status=RegistrationStatus.INCOMPLETE,
        created_at=datetime(2024, 12, 1, 10, 0, 0),
        updated_at=datetime(2024, 12, 2, 14, 15, 0),
    )

    dto = OutputCustomerDTO.from_domain(customer_entity)

    assert dto.id == "123455"
    assert dto.name == "Jane Doe"
    assert dto.email == "jane.doe@example.com"
    assert dto.national_id == "987654321"
    assert dto.registration_status == "INCOMPLETE"
    assert dto.created_at == "2024-12-01T10:00:00Z"
    assert dto.updated_at == "2024-12-02T14:15:00Z"


def test_to_dict():
    dto = OutputCustomerDTO(
        id="12345",
        name="John Doe",
        email="john.doe@example.com",
        national_id="123456789",
        registration_status="COMPLETED",
        created_at="2024-12-02T12:30:00Z",
        updated_at=None,
    )

    dto_dict = dto.to_dict()

    assert isinstance(dto_dict, dict)
    assert dto_dict["id"] == "12345"
    assert dto_dict["name"] == "John Doe"
    assert dto_dict["email"] == "john.doe@example.com"
    assert dto_dict["national_id"] == "123456789"
    assert dto_dict["registration_status"] == "COMPLETED"
    assert dto_dict["created_at"] == "2024-12-02T12:30:00Z"
    assert "updated_at" not in dto_dict

    dto.updated_at = "2024-12-02T14:15:00Z"
    dto_dict_with_updated_at = dto.to_dict()
    assert dto_dict_with_updated_at["updated_at"] == "2024-12-02T14:15:00Z"
