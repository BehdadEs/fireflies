from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timezone
from typing import Any


class Method(str, Enum):
    POST = "post"
    GET = "get"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"


class Operator(str, Enum):
    EQUAL = "equal"
    NOT_EQUAL = "not-equal"
    GREATER_THAN = "greater-than"
    LESS_THAN = "less-than"
    GREATER_THAN_OR_EQUAL = "greater-than-equal"
    LESS_THAN_OR_EQUAL = "less-than-equal"


class XOR(str, Enum):
    AND = "and"
    OR = "or"


class ConditionItem(BaseModel):
    field: str
    operator: Operator
    value: str | int | float | bool | dict | list[str | int | float | bool]


class Condition(BaseModel):
    items: list[ConditionItem]
    bitwise: XOR | None = None
    status_code: int = Field(gt=100, lt=600)
    response_body: dict


class AddEndpoint(BaseModel):
    endpoint: str
    method: Method
    default_status_code: int = Field(gt=100, lt=600)
    conditions: list[Condition] | None = None
    default_response_body: Any
    sleep: float | None = None
    tag: str | None = None


class EndpointResponse(BaseModel):
    id: int
    endpoint: str
    method: str
    conditions: list[Condition] | None = None
    default_response_body: Any
    default_status_code: int = Field(gt=100, lt=600)
    sleep: float | None = None
    tag: str | None = None


class AddEndpointResponse(BaseModel):
    status: str
    endpoint: EndpointResponse


class AllEndpointResponse(BaseModel):
    status: str
    endpoints: list[EndpointResponse]


class Log(BaseModel):
    created_at: datetime
    status_code: int
    response_body: dict
    request_body: dict | None = None
    default_data: bool
    evaluation_match: bool
    matched_condition: dict | None = None


class LogResponse(BaseModel):
    status: str
    items: list[Log]

    class Config:
        from_attributes = True
