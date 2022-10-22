import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(__file__)
app = FastAPI()
templates = Jinja2Templates(directory = f"{BASE_DIR}/templates")

@app.get("/",response_class=HTMLResponse) #http GET
def home_view(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post("/") # http POST
def home_detail_view():
    return {"hello":"world"}