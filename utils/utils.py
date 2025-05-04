import re
import json
from json.decoder import JSONDecodeError
from fastapi import HTTPException, status
from models.model import EndpointData
from utils.config import CONFIG


def create_endpoint(data: dict) -> EndpointData:
    endpoint = data
    endpoint["method"] = endpoint["method"].value.upper()
    valid_endpoint = validate_path(endpoint["endpoint"])
    if not valid_endpoint:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Endpoint should start with (/)"},
        )
    if endpoint["sleep"] and endpoint["sleep"] > 60:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Sleep should be less than 60 seconds"},
        )
    conditions = endpoint["conditions"]
    if conditions and len(conditions) > 0:
        expression_list = []
        for condition in conditions:
            expression_list.append(json_to_condition(condition))
        endpoint["expression_strings"] = expression_list
    else:
        endpoint["expression_strings"] = []
    endpoint_instance = EndpointData(**endpoint)
    return endpoint_instance


def json_to_condition(json_data: dict):
    # check if input is json or dict
    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
    except JSONDecodeError:
        raise Exception("Can't parse JSON")
    except Exception as e:
        raise Exception(f"Something went wrong: {e}")

    conditions = data.get("items", [])
    bitwise = data.get("bitwise")

    def parse_condition(condition: dict):
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]

        operation_map = {
            "equal": "==",
            "not-equal": "!=",
            "greater-than": ">",
            "less-than": "<",
            "greater-than-equal": ">=",
            "less-than-equal": "<=",
        }

        python_operation = operation_map.get(operator, None)
        if python_operation is None:
            raise ValueError(f"Unknown operator: {operator}")

        if isinstance(value, str):
            value = f"'{value}'"

        return f"data.get('{field}', None) {python_operation} {value}"

    parsed_conditions = [parse_condition(cond) for cond in conditions]

    # if no bitwise is provided and there are more than one condition "and" will be used
    if bitwise == "and" or (bitwise is None and len(parsed_conditions) > 1):
        return " and ".join(parsed_conditions)
    elif bitwise == "or":
        return " or ".join(parsed_conditions)
    else:
        return parsed_conditions[0]


def validate_path(v: str):
    if not re.match(r"^/", v):
        return False
    return v


def check_token(api_key: str, token_type: str):
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if token_type == "admin":
        if api_key != CONFIG["admin_token"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif token_type == "mock":
        if api_key != CONFIG["mock_token"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
