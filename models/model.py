class EndpointData:
    def __init__(
        self,
        endpoint: str,
        method: str,
        default_status_code: int,
        default_response_body: dict,
        sleep: float,
        tag: str,
        conditions: list,
        expression_strings: list,
    ):
        self.endpoint = endpoint
        self.method = method
        self.default_status_code = default_status_code
        self.default_response_body = default_response_body
        self.sleep = sleep
        self.tag = tag
        self.conditions = conditions
        self.expression_strings = expression_strings
