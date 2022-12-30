import os
import io
import uuid
from fastapi import (FastAPI,
                    Depends,
                    Request,
                    File,
                    UploadFile,
                    HTTPException)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    debug:bool = False
    echo_active:bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG = settings.debug

BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR,'uploads')
print(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR,exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory = os.path.join(BASE_DIR,'templates'))

@app.get("/",response_class=HTMLResponse) #http GET
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post("/") # http POST
def home_detail_view():
    return {"hello":"world"}

@app.post("/img_echo",response_class=FileResponse)
async def img_echo_view(file:UploadFile= File(...),settings:Settings = Depends(get_settings)):
    print(settings.echo_active)
    if not settings.echo_active:
        raise HTTPException(status_code = 404, detail= 'Invalid endpoint.')

    file_bytes_str = io.BytesIO(await file.read())
    # save the byte stream
    _,fsuffix = os.path.splitext(file.filename)
    dest = os.path.join(UPLOAD_DIR,f"{uuid.uuid1()}{fsuffix}")
    with open(dest, 'wb') as out:
        out.write(file_bytes_str.read())
    
    return dest