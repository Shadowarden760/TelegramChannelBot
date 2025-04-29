from pydantic import BaseModel, Field


class BotLogModel(BaseModel):
    status: bool = Field(description="event status")
    action: str = Field(description="event")
    data: dict = Field(description="action data")


