import pytest
from PIL import Image
import os

#sample test function 
def  test_image_exist():
    assert os.path.exists("images/image1.JPG")

def test_image_open():

    try:
        img = Image.open("images/image1.JPG")
        img.verify()
        assert True
    except:
        assert False