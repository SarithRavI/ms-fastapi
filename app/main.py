import os
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    debug:bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG = settings.debug

BASE_DIR = os.path.dirname(__file__)
app = FastAPI()
templates = Jinja2Templates(directory = f"{BASE_DIR}/templates")

@app.get("/",response_class=HTMLResponse) #http GET
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post("/") # http POST
def home_detail_view():
    return {"hello":"world"}