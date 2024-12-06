import os
from typing import Dict, List, Optional

from pymongo import MongoClient
from pymongo.server_api import ServerApi


from domain.entities import CustomerEntity
from ports.repositories import CustomerRepositoryInterface

username = os.environ.get("DATABASE_MONGO_USER")
password = os.environ.get("DATABASE_MONGO_PASSWORD")
host = os.environ.get("DATABASE_MONGO_HOST")
database = os.environ.get("DATABASE_MONGO_DATABASE")

uri = f"mongodb+srv://{username}:{password}@{host}/{database}"

client = MongoClient(uri, server_api=ServerApi("1"))

db = client.get_database()
collection = db["customers"]


class CustomerMongodbRepository(CustomerRepositoryInterface):

    def create(self, customer_entity: CustomerEntity) -> CustomerEntity:
        customer = collection.insert_one(customer_entity.as_dict())
        customer_entity.id = str(customer.inserted_id)
        return customer_entity

    def list(self) -> List[CustomerEntity] | None:
        customers = list(collection.find({}))
        if not customers:
            return None
        customerList = []
        for customer in customers:
            customerList.append(
                CustomerEntity.from_dict(
                    {
                        "id": str(customer["_id"]),
                        "name": customer.get("name"),
                        "email": customer.get("email"),
                        "national_id": customer.get("national_id"),
                        "registration_status": customer.get("registration_status"),
                        "created_at": customer.get("created_at"),
                        "updated_at": customer.get("updated_at"),
                    }
                )
            )

        return customerList

    def find_customer_by_national_id(self, national_id: str) -> Optional[Dict]:
        customer = collection.find_one({"national_id": national_id})
        if not customer:
            return None
        return {
            "id": str(customer["_id"]),
            "name": customer.get("name"),
            "email": customer.get("email"),
            "national_id": customer.get("national_id"),
            "registration_status": customer.get("registration_status"),
            "created_at": customer.get("created_at"),
            "updated_at": customer.get("updated_at"),
        }

    def get_by_id(self, customer_id: int) -> CustomerEntity | None:
        pass
        # customer = CustomerModel.get_or_none(id=customer_id)
        # if not customer:
        #     return None
        # return CustomerEntity(**customer.model_to_dict())
