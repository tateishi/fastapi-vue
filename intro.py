from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def hello():
    return dict(text='hello world!')


@app.get('/get/{path}')
async def path_and_query_params(
    path: str,
    query: int,
    default_none: Optional[str] = None):
    return dict(text=f'hello, {path}, {query} and {default_none}')
