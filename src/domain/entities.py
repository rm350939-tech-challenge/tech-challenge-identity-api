from enum import Enum
from datetime import datetime
from typing import Dict
from dataclasses import dataclass, asdict, field

from domain.value_objects import NationalID, Email


class RegistrationStatus(Enum):
    COMPLETED = 1
    INCOMPLETE = 2
    PENDING = 3

    @classmethod
    def from_value(cls, value):
        return cls(value=value)


@dataclass
class CustomerEntity:
    id: int = field(default=None, repr=False, kw_only=True)
    name: str
    email: Email
    national_id: NationalID
    registration_status: RegistrationStatus
    created_at: datetime = field(default=datetime.now(), kw_only=True)
    updated_at: datetime = field(default=None, kw_only=True)

    def as_dict(self) -> Dict:
        serialized = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
        serialized["email"] = self.email.value
        serialized["national_id"] = self.national_id.value
        serialized["registration_status"] = self.registration_status.value
        return serialized

    @classmethod
    def from_dict(cls, data: Dict):
        data_copy = data
        data_copy["email"] = Email(data["email"])
        data_copy["national_id"] = NationalID(data["national_id"])
        data_copy["registration_status"] = RegistrationStatus(
            data["registration_status"]
        )
        return cls(**data_copy)
