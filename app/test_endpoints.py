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

def test_faulty_prediction():
    response = client.post("/")
    assert response.status_code==422
    assert 'application/json' in response.headers['content-type']

def test_response_prediction():
    test_images_path = os.path.join(BASE_DIR,'test_images')
    for path in os.listdir(test_images_path):
        test_img_path = os.path.join(test_images_path,path)
        test_img = open(test_img_path,'rb')
        response = client.post("/",files={'file':test_img},headers = {'authentication':'bearer BxD11Z3SEjcyFYz3MWGJIA'})
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


def test_echo_img():
    test_images_path = os.path.join(BASE_DIR,'test_images')
    for path in os.listdir(test_images_path):
        test_img_path = os.path.join(test_images_path,path)
        test_img = open(test_img_path,'rb')
        response = client.post("/img_echo",files={'file':test_img})
        byte_str = io.BytesIO(response.content)
        try:
            test_img = Image.open(test_img_path)
            uploaded_img = Image.open(byte_str)
        except:
            test_img = None
            # uploaded_img = None
        
        if  test_img is None:
            assert response.status_code == 404

        # elif uploaded_img is None:
        #     pass

        else:
            # checking if the test and uploaded images are the same 
            diff = ImageChops.difference(test_img, uploaded_img).getbbox()
            assert diff is None
            assert response.status_code == 200
            # response.headers['content-type'] == 'image/png'
            # by using following we can allow any type of image
            assert 'image/' in response.headers['content-type']  
    shutil.rmtree(UPLOAD_DIR)

