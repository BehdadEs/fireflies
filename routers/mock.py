from fastapi import status, HTTPException, Depends, APIRouter, Request, Response
from sqlalchemy.orm import Session
from database.db import get_db
from database import models
from asyncio import sleep

router = APIRouter(tags=["Mocking API"])


@router.api_route(
    "/{endpoint_url:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def mock(
    request: Request,
    endpoint_url: str,
    response: Response,
    req_body: dict | None = None,
    db: Session = Depends(get_db),
):
    requested_endpoint = f"/{endpoint_url}"
    endpoint_data = (
        db.query(models.Endpoints)
        .filter(models.Endpoints.endpoint == requested_endpoint)
        .first()
    )
    if not endpoint_data or endpoint_data.method != request.method:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    log = {
        "status_code": endpoint_data.default_status_code,
        "response_body": endpoint_data.default_response_body,
        "request_body": req_body,
        "default_data": True,
        "evaluation_match": False,
        "matched_condition": None,
        "endpoint_id": endpoint_data.id,
    }

    def write_log(log_data: dict):
        new_log = models.Logs(**log_data)
        db.add(new_log)
        db.commit()

    def return_default():
        write_log(log)
        response.status_code = endpoint_data.default_status_code
        return endpoint_data.default_response_body

    if endpoint_data.sleep and endpoint_data.sleep > 0:
        await sleep(endpoint_data.sleep)

    if not endpoint_data.conditions:
        return return_default()

    data = req_body
    expr_strs = endpoint_data.expression_strings
    for index, expr_str in enumerate(expr_strs):
        try:
            evaluation = eval(expr_str, {"__builtins__": {}}, {"data": data})
            if evaluation:
                log["evaluation_match"] = True
                log["default_data"] = False
                log["status_code"] = endpoint_data.conditions[index]["status_code"]
                log["response_body"] = endpoint_data.conditions[index]["response_body"]
                log["matched_condition"] = endpoint_data.conditions[index]
                write_log(log)
                response.status_code = endpoint_data.conditions[index]["status_code"]
                return endpoint_data.conditions[index]["response_body"]
        except Exception:
            continue
    return return_default()
