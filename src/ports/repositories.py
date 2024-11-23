from typing import Optional, Dict, List
from abc import ABC, abstractmethod

from domain.entities import CustomerEntity


class CustomerRepositoryInterface(ABC):

    @abstractmethod
    def create(self, customer_entity: CustomerEntity) -> Optional[CustomerEntity]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[CustomerEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_customer_by_national_id(self, national_id: str) -> Optional[Dict]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, customer_id: int) -> CustomerEntity | None:
        raise NotImplementedError
