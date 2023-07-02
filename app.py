import os
from fastapi import FastAPI
from utils import *
from pydantic import BaseModel

app = FastAPI()

class ResponseModel(BaseModel):
    pages: list
    total_time: float

@app.post("/gcp_vision")
def extract_text_gcp():
    response = detect_text_from_page_google_vision("./output/")
    return response

@app.post("/tesseract_single")
def extract_text_tesseract_single():
    response = detect_text_from_page_tesseract_single_thread("./output/")
    return response

@app.post("/tesseract_multi")
def extract_text_tesseract_multi():
    responsesingle = detect_text_from_page_tesseract_single_thread("./output/")
    responsemulti = detect_text_from_page_tesseract_multi_thread("./output/")
    return responsesingle, responsemulti
