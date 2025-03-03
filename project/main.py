import asyncio

import uvicorn
from fastapi import FastAPI

from config import get_settings
from api import channel

settings = get_settings()

app = FastAPI()
app.include_router(router=channel.router)


async def main():
    if settings.DEBUG:
        uvicorn.run(app="main:app", reload=True, proxy_headers=True, host="0.0.0.0", port=settings.WEB_PORT)
    else:
        uvicorn.run(app="main:app", proxy_headers=True, host="0.0.0.0", port=settings.WEB_PORT, workers=4)


if __name__ == "__main__":
    asyncio.run(main())
