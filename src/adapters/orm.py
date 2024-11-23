import os
from typing import Dict, List, Optional
from datetime import datetime

from domain.entities import CustomerEntity
from ports.repositories import CustomerRepositoryInterface

from playhouse.shortcuts import model_to_dict
from peewee import (
    PostgresqlDatabase,
    Model,
    CharField,
    DateTimeField,
    SmallIntegerField,
)

db = PostgresqlDatabase(
    database=os.environ.get("DATABASE_NAME"),
    host=os.environ.get("DATABASE_HOST"),
    port=os.environ.get("DATABASE_PORT"),
    user=os.environ.get("DATABASE_USER"),
    password=os.environ.get("DATABASE_PASSWORD"),
)


class CustomerModel(Model):
    name: str = CharField(max_length=120)
    email: str = CharField(max_length=80)
    national_id: str = CharField(max_length=11, unique=True)
    registration_status: int = SmallIntegerField()
    created_at: datetime = DateTimeField()
    updated_at: datetime = DateTimeField(null=True)

    def model_to_dict(self) -> Dict:
        return model_to_dict(self)

    class Meta:
        database = db
        table_name = "customers"


class CustomerRepository(CustomerRepositoryInterface):

    def create(self, customer_entity: CustomerEntity) -> CustomerModel:
        customer = CustomerModel(**customer_entity.as_dict())
        customer.save()
        return customer

    def list(self) -> List[CustomerEntity] | None:
        customers = CustomerModel.select()
        if not customers:
            return None
        return [
            CustomerEntity.from_dict(data=customer.model_to_dict())
            for customer in customers
        ]

    def find_customer_by_national_id(self, national_id: str) -> Optional[Dict]:
        customer = CustomerModel.get_or_none(national_id=national_id)
        if not customer:
            return None
        return customer.model_to_dict()

    def get_by_id(self, customer_id: int) -> CustomerEntity | None:
        customer = CustomerModel.get_or_none(id=customer_id)
        if not customer:
            return None
        return CustomerEntity(**customer.model_to_dict())
