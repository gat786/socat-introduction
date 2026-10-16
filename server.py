"""Tiny HTTP server for demoing raw HTTP requests with socat.

Run:   uv run server.py          (listens on 127.0.0.1:8000)
"""

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI(title="socat demo server")

ALL_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]


@app.api_route("/", methods=ALL_METHODS, response_class=PlainTextResponse)
async def any_method(request: Request) -> str:
    """Accepts any method and says which one it received."""
    body = await request.body()
    msg = f"You made a {request.method} request to {request.url.path}\n"
    if body:
        msg += f"Your request had a {len(body)}-byte body: {body.decode(errors='replace')}\n"
    return msg


class Message(BaseModel):
    name: str
    message: str


@app.post("/json")
async def parse_json(payload: Message) -> dict:
    """Requires a JSON body like {"name": "...", "message": "..."} and echoes it back parsed."""
    return {
        "status": "ok",
        "received": payload.model_dump(),
        "reply": f"Hello {payload.name}, you said: {payload.message}",
    }


@app.api_route("/inspect", methods=ALL_METHODS, response_class=PlainTextResponse)
async def inspect(request: Request) -> str:
    """Shows what the server parsed out of your raw bytes: method, path, query, headers, body."""
    body = await request.body()
    lines = [
        f"method : {request.method}",
        f"path   : {request.url.path}",
        f"query  : {dict(request.query_params)}",
        "headers:",
        *(f"  {k}: {v}" for k, v in request.headers.items()),
        f"body   : {body!r}",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
