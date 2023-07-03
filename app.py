import os
from fastapi import FastAPI, UploadFile, File
from utils import *
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",
    # Add more allowed origins as needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
class ResponseModel(BaseModel):
    pages: list
    total_time: float

UPLOAD_DIR = "./"

path_to_files = []

folder_name = "output"

# Create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Folder '{folder_name}' created successfully.")
else:
    print(f"Folder '{folder_name}' already exists.")

for filename in os.listdir("./output/"):
    path_to_files.append(os.path.join("./output/", filename))

path_to_files.sort()

@app.post("/gcp_vision")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to the upload directory
    print(file, "file")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        contents = await file.read()
        binary_contents = bytearray(contents)  # Convert array buffer to binary data
        f.write(binary_contents)
    print({"filename": file.filename, "message": "File uploaded successfully"})
    await convert_to_images(file.filename)
    response =  await extract_text_gcp()
    return response
async def extract_text_gcp():
    response = await detect_text_from_page_google_vision(path_to_files)
    return response

@app.post("/tesseract_single")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to the upload directory
    print(file, "file")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        contents = await file.read()
        binary_contents = bytearray(contents)  # Convert array buffer to binary data
        f.write(binary_contents)
    print({"filename": file.filename, "message": "File uploaded successfully"})
    await convert_to_images(file.filename)
    response =  await extract_text_tesseract_single()
    return response

async def extract_text_tesseract_single():
    response = await detect_text_from_page_tesseract_single_thread(path_to_files)
    return response


@app.post("/tesseract_multi")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to the upload directory
    print(file, "file")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        contents = await file.read()
        binary_contents = bytearray(contents)  # Convert array buffer to binary data
        f.write(binary_contents)
    print({"filename": file.filename, "message": "File uploaded successfully"})
    await convert_to_images(file.filename)
    response = await extract_text_tesseract_multi()
    return response

async def extract_text_tesseract_multi():
    responsesingle = await detect_text_from_page_tesseract_single_thread(path_to_files)
    responsemulti = await detect_text_from_page_tesseract_multi_thread(path_to_files)
    page_text = []
    for p in responsesingle["pages"]:
        page_text.append(p['page_text'])

    output = {
        "single_thread_time": responsesingle["totaltime"],
        "multi_thread_time": responsemulti,
        "page_text": page_text
    }
    return output
