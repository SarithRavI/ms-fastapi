import os
from app.main import app, BASE_DIR
from fastapi.testclient import TestClient

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
    test_images_path = os.path.join(f'{BASE_DIR}/test_images')
    for path in os.listdir(test_images_path):
        response = client.post("/img_echo",files={'file':open(f'{test_images_path}/{path}','rb')})
        assert response.status_code==200
        assert response.headers['content-type'] == 'image/png'