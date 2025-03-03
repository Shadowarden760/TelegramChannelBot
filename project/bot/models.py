from typing import Union

from pydantic import BaseModel, Field


class BotLogModel(BaseModel):
    message_id: Union[int, None] = Field(description="chat message id", default=None)
    message_text: Union[str, None] = Field(description="chat message text", default=None)
    action: str = Field(description="event")
    status: bool = Field(description="event status")
