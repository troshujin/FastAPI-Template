from pydantic import BaseModel


class CorrelationIDSchema(BaseModel):
    correlation_id: str
