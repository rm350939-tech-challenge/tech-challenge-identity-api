from typing import Optional
from pydantic import BaseModel

from domain.entities import CustomerEntity


class OutputCustomerDTO(BaseModel):
    id: int
    name: str
    email: str
    national_id: str
    registration_status: str
    created_at: str
    updated_at: Optional[str] = None

    @classmethod
    def from_domain(cls, customer: CustomerEntity):
        return cls(
            id=customer.id,
            name=customer.name,
            email=customer.email.value,
            national_id=customer.national_id.value,
            registration_status=customer.registration_status.name,
            created_at=customer.created_at.strftime(format="%Y-%m-%dT%H:%M:%SZ"),
            updated_at=(
                customer.updated_at.strftime(format="%Y-%m-%dT%H:%M:%SZ")
                if customer.updated_at
                else None
            ),
        )

    def to_dict(self):
        return self.model_dump(exclude_none=True)
