import os
import io
from app.main import app, BASE_DIR,UPLOAD_DIR
from fastapi.testclient import TestClient
import shutil
from PIL import Image,ImageChops
import requests
from .main import get_settings

client = TestClient(app)
settings = get_settings()

PROD_ENDPOINT = ""

def test_get_home():
    response = requests.get(PROD_ENDPOINT)
    assert response.status_code==200
    assert 'text/html' in response.headers['content-type']

def test_faulty_prediction():
    response = requests.post(PROD_ENDPOINT)
    assert response.status_code==422
    assert 'application/json' in response.headers['content-type']

def test_faulty_header():
    test_images_path = os.path.join(BASE_DIR,'test_images')
    ex_path =  os.listdir(test_images_path)[0]
    test_img_path = os.path.join(test_images_path,ex_path)
    test_img = open(test_img_path,'rb')
    response = requests.post(PROD_ENDPOINT,files={'file':test_img},headers = {'authentication':'bearer this-is-a-faulty-token'})
    assert response.status_code == 401

def test_response_prediction():
    test_images_path = os.path.join(BASE_DIR,'test_images')
    for path in os.listdir(test_images_path):
        test_img_path = os.path.join(test_images_path,path)
        test_img = open(test_img_path,'rb')
        response = requests.post(PROD_ENDPOINT,files={'file':test_img},headers = {'authentication':f'bearer {settings.access_token_prod}'})
        try:
            if '-faulty' in test_img_path:
                test_img = None
            else:
                test_img = Image.open(test_img_path)  
        except:
            test_img = None
        if test_img is None:
            assert response.status_code == 404  
        else:
            assert response.status_code == 200
            data = response.json()
            assert list(data.keys()) == ['text','sentences']
            # response.headers['content-type'] == 'image/png'
            # by using following we can allow any type of image
            assert 'application/json' in response.headers['content-type'] 


