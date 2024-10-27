from http.client import HTTPException
from mailbox import Message
from fastapi import FastAPI, Path, Request
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.v1 import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
async def main(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html",{"request":request,"users":users})

@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")


@app.post("/")
async def create_user(request: Request, username: str, age: int)-> HTMLResponse:
    last_id = users[-1].id if users else 0
    new_id = last_id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html",{"request":request,"message":users})


##@app.put("/user/{user_id}/{username}/{age}")
##async def update_user(user_id: int, username: str, age: int):
 ##   for i, user in enumerate(users):
 ##       if user.id == user_id:
 ##           users[i].username = username
 ##           users[i].age = age
 ##           return users[i]
  ##  raise HTTPException(status_code=404, detail="User was not found")


##@app.delete("/user/{user_id}")
##async def delete_user(user_id: int):
##    for i, user in enumerate(users):
##        if user.id == user_id:
##            deleted_user = users.pop(i)
##            return deleted_user
##    raise HTTPException(status_code=404, detail="User was not found")