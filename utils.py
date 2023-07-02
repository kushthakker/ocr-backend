import os
from PIL import Image
import pytesseract
import cv2
import threading
from prettytable import PrettyTable
from tqdm import tqdm
import time
from pytesseract import Output
from google.cloud import vision
from google.cloud import storage
import pypdfium2 as pdfium

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './auth.json'

# Initializing Google Vision API client
vision_client = vision.ImageAnnotatorClient()


async def convert_to_images(pdf_path):
    # Convert each page of the PDF to images
    pdf = pdfium.PdfDocument(pdf_path)
    n_pages = len(pdf)
    loading_bar = tqdm(total=n_pages, desc="Generating images from PDF")

    for i in range(len(pdf)):
        filename = str(i) + ".png"
        page = pdf.get_page(i)
        pil_image = page.render(scale=300/72).to_pil()
        pil_image.save(f"./output/{filename}")
        loading_bar.update(1)
    loading_bar.close()


async def detect_text_from_page_google_vision(path_to_images):
    # Perform text detection using Google Vision API
    response_dictionary = {"pages": []}
    text_on_page = []
    time_taken_per_page = []
    total_time = time.time()

    for path_to_image in path_to_images:
        file_name = os.path.abspath(path_to_image)

        with open(file_name, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        starttime = time.time()
        response = vision_client.text_detection(image=image)
        endtime = time.time()

        response = response.text_annotations[0].description

        text_on_page.append(response)
        time_taken_per_page.append(endtime - starttime)

    totaltime = time.time() - total_time

    for i in range(0, len(text_on_page)):
        dummy_dictionary = {
            "page": i + 1,
            "page_text": text_on_page[i],
            "page_time": time_taken_per_page[i]
        }
        response_dictionary["pages"].append(dummy_dictionary)
    response_dictionary["totaltime"] = totaltime
    return response_dictionary


async def detect_text_from_page_tesseract_single_thread(path_to_images):
    #text detection using Tesseract OCR (single-threaded)
    loading_bar = tqdm(total=len(path_to_images), desc="Processing Images")
    response_dictionary = {"pages": []}
    text_on_page = []
    time_taken_per_page = []
    total_time = time.time()

    for path_to_image in path_to_images:
        file_name = os.path.abspath(path_to_image)

        image = cv2.imread(file_name)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        starttime = time.time()
        results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
        endtime = time.time()

        response = ""
        for result in results["text"]:
            response = response + " " + result

        text_on_page.append(response)
        time_taken_per_page.append(endtime - starttime)
        loading_bar.update(1)
        
    totaltime = time.time() - total_time

    for i in range(0, len(text_on_page)):
        dummy_dictionary = {
            "page": i + 1,
            "page_text": text_on_page[i],
            "page_time": time_taken_per_page[i]
        }
        response_dictionary["totaltime"] = totaltime
        response_dictionary["pages"].append(dummy_dictionary)
    loading_bar.close()
    return response_dictionary


async def detect_text_from_page_tesseract_multi_thread(path_to_images):
    # Perform text detection using Tesseract OCR (multi-threaded)
    response_dictionary = {"pages": []}
    text_on_page = [None] * len(path_to_images)
    time_taken_per_page = [None] * len(path_to_images)
    total_time = time.time()

    def process_page(pagenumber, image):
        starttime = time.time()
        results = pytesseract.image_to_data(image, output_type=Output.DICT)
        response = ""
        for result in results["text"]:
            response = response + " " + result
        endtime = time.time() - starttime
        text_on_page[pagenumber] = response
        time_taken_per_page[pagenumber] = endtime

    with tqdm(total=len(path_to_images), desc="Processing Images", unit="image") as pbar:
        threads = []
        for pagenumber, path_to_image in enumerate(path_to_images):
            file_name = os.path.abspath(path_to_image)
            image = cv2.imread(file_name)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            thread = threading.Thread(target=process_page, args=(pagenumber, image))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            pbar.update(1)

    totaltime = time.time() - total_time

    for i in range(0, len(text_on_page)):
        dummy_dictionary = {
            "page": i + 1,
            "page_text": text_on_page[i],
            "page_time": time_taken_per_page[i]
        }
        response_dictionary["pages"].append(dummy_dictionary)
        response_dictionary["total_time"] = totaltime
    # creating table to print to console
    return totaltime

def count_items_in_directory(directory_path):
    total_items = 0

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            total_items += 1  # Include directories in the count
        elif os.path.isfile(item_path):
            total_items += 1  # Include files in the count

    return total_items
