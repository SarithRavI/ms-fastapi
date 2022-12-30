import os
import io
from app.main import app, BASE_DIR,UPLOAD_DIR
from fastapi.testclient import TestClient
import shutil
from PIL import Image,ImageChops

client = TestClient(app)

def test_get_home():
    response = client.get("/")
    assert response.status_code==200
    assert 'text/html' in response.headers['content-type']

def test_post_home():
    response = client.post("/")
    assert response.status_code==200
    assert 'application/json' in response.headers['content-type']

def test_echo_img():
    test_images_path = os.path.join(BASE_DIR,'test_images')
    for path in os.listdir(test_images_path):
        test_img = open(os.path.join(test_images_path,path),'rb')
        response = client.post("/img_echo",files={'file':test_img})
        byte_str = io.BytesIO(response.content)
        try:
            test_img = Image.open(os.path.join(test_images_path,path))
            uploaded_img = Image.open(byte_str)
        except:
            uploaded_img = None
        if uploaded_img is None:
            assert response.status_code == 404
        else:
            # checking if the test and uploaded images are the same 
            diff = ImageChops.difference(test_img, uploaded_img).getbbox()
            assert diff is None
            assert response.status_code == 200
            assert response.headers['content-type'] == 'image/png'    
    shutil.rmtree(UPLOAD_DIR)

