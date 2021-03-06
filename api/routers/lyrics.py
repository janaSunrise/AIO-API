from fastapi import APIRouter, Request

from api import http_client
from api.core import log_error

router = APIRouter(
    prefix="/lyrics",
    tags=["Song lyrics endpoint"],
    responses={
        404: {"description": "Not found"},
    },
)


# -- Router paths --
@router.get("/")
@log_error()
async def lyrics(_: Request, songname: str) -> dict:
    """Get the lyrics for some song which you need."""
    async with http_client.session.get(
        f"https://some-random-api.ml/lyrics?title={songname}"
    ) as resp:
        json = await resp.json()

    return {
        "title": json["title"],
        "author": json["author"],
        "lyrics": json["lyrics"],
        "thumbnail": json["thumbnail"]["genius"],
    }
