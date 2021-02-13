import random

from fastapi import APIRouter

from api.app import http_client

router = APIRouter(
    prefix="/fun",
    tags=["fun"],
    responses={
        404: {"description": "Not found"},
    },
)


# -- Router paths --
@router.get("/joke")
async def joke(explicit: bool = False):
    if explicit:
        url = "http://api.icndb.com/jokes/random"
    else:
        url = "http://api.icndb.com/jokes/random?exclude=[explicit]"

    async with http_client.session.get(url) as resp:
        json = await resp.json()

    return {
        "joke": json["value"]["joke"].replace("&quote", '"')
    }


@router.get("/dadjoke")
async def dadjoke():
    async with http_client.session.get("https://icanhazdadjoke.com") as resp:
        res = await joke.text()
        res = res.encode("utf-8").decode("utf-8")

    return {
        "joke": res
    }


@router.get("/excuse")
async def excuse():
    async with http_client.session.get("http://pages.cs.wisc.edu/~ballard/bofh/excuses") as resp:
        data = await resp.text()
        lines = data.split("\n")

    return {
        "excuse": random.choice(lines)
    }


@router.get("/chucknorris")
async def chucknorris():
    async with http_client.session.get("https://api.chucknorris.io/jokes/random") as resp:
        json = await resp.json()

    return {
        "joke": json["value"]
    }


@router.get("/why")
async def why():
    async with http_client.session.get("https://nekos.life/api/why") as resp:
        json = await resp.json()

    return {
        "why": json["why"]
    }


@router.get("/yesno")
async def yesno(question: str):
    async def get_answer(ans: str) -> str:
        if ans == "yes":
            return_str = "Yes."
        elif ans == "no":
            return_str = "NOPE"
        elif ans == "maybe":
            return_str = "maaaaaaybe?"
        else:
            return_str = "Internal Error: Invalid answer LMAOO"

        return return_str

    async with http_client.session.get("https://yesno.wtf/api") as resp:
        json = await resp.json()

    return {
        "question": question,
        "answer": get_answer(json["answer"])
    }


@router.get("/history")
async def history():
    async with http_client.session.get('http://numbersapi.com/random/date?json') as resp:
        json = await resp.json()

    return {
        "fact": json["text"],
        "year": json["year"]
    }


@router.get("/mathfact")
async def mathfact():
    async with http_client.session.get('http://numbersapi.com/random/math?json') as resp:
        json = await resp.json()

    return {
        "fact": json["text"],
        "number": json["number"]
    }


@router.get("/advice")
async def advice():
    async with http_client.session.get("https://api.adviceslip.com/advice") as resp:
        json = await resp.json(content_type="text/html")

    return {
        "advice": json["slip"]["advice"]
    }