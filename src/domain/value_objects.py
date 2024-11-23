from dataclasses import dataclass


@dataclass(frozen=True)
class NationalID:
    value: str


@dataclass(frozen=True)
class Email:
    value: str
