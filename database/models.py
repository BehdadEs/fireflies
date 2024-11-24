from database.db import Base
from sqlalchemy.sql.sqltypes import (
    Integer,
    String,
    TIMESTAMP,
    JSON,
    Float,
    Boolean,
    ARRAY,
)
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.expression import text


class Endpoints(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, nullable=False)
    endpoint = Column(String, nullable=False, unique=True)
    method = Column(String, nullable=False)
    default_status_code = Column(Integer, nullable=False)
    default_response_body = Column(JSON, nullable=False)
    sleep = Column(Float, server_default="0")
    tag = Column(String, nullable=True)
    conditions = Column(ARRAY(JSON), nullable=True)
    expression_strings = Column(ARRAY(String), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, nullable=False)
    status_code = Column(Integer, nullable=False)
    response_body = Column(JSON, nullable=False)
    request_body = Column(JSON, nullable=True)
    default_data = Column(Boolean, nullable=False)
    evaluation_match = Column(Boolean, nullable=False)
    matched_condition = Column(JSON, nullable=True)
    endpoint_id = Column(Integer, ForeignKey("endpoints.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
