import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='./auth.json'
from google.cloud import vision
import re
from PIL import Image
vision_client = vision.ImageAnnotatorClient()
import json
import re
from google.cloud import vision
from google.cloud import storage
import pypdfium2 as pdfium
import time
from pytesseract import Output
import pytesseract
import cv2
import threading
from utils import *
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# convert_to_images("./12100010_f1.pdf")

path_to_files = []

for filename in os.listdir("./output/"):
    path_to_files.append(os.path.join("./output/", filename))

path_to_files.sort()

# @app.post("/gcp_vision")
option = input("select type of task you want to run\n 1) Local Teseract\n 2) Google Vision\n")
if option == "1":
    teserract_option = input("1)Single Thread\n2) Multithread\n")
    if teserract_option == "1":
        print(f"Starting {teserract_option}")
        def extract_text_tesseract_single():
            response = detect_text_from_page_tesseract_single_thread(path_to_files)
            # print(response)
        extract_text_tesseract_single()
    elif teserract_option == "2":
        def extract_text_tesseract_single():
            # responsesingle = detect_text_from_page_tesseract_single_thread(path_to_files)
            responsemulti = detect_text_from_page_tesseract_multi_thread(path_to_files)
            # return responsesingle, responsemulti
        extract_text_tesseract_single()
elif option == "2":
    def extract_text_gcp():
        response = detect_text_from_page_google_vision(path_to_files)
        return response
    extract_text_gcp()
        
# async def extract_text_gcp():
#     response = detect_text_from_page_google_vision(path_to_files)
#     return response

# @app.post("/tesseract_single")
# async def extract_text_tesseract_single():
#     response = detect_text_from_page_tesseract_single_thread(path_to_files)
#     return response

# @app.post("/tesseract_multi")
# async def extract_text_tesseract_single():
#     responsesingle = detect_text_from_page_tesseract_single_thread(path_to_files)
#     responsemulti = detect_text_from_page_tesseract_multi_thread(path_to_files)
#     return responsesingle, responsemulti


    