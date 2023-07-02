import os
from utils import *
from pydantic import BaseModel



# convert_to_images("./12100010_f1.pdf")

path_to_files = []

for filename in os.listdir("./output/"):
    path_to_files.append(os.path.join("./output/", filename))

path_to_files.sort()


option = input("select type of task you want to run:\n 1) Local Teseract\n 2) Google Vision\n")
if option == "1":
    teserract_option = input("1) Single Thread\n2) Singlethread + Multithread (Compare)\n")
    if teserract_option == "1":
        print(f"Starting {teserract_option}")
        def extract_text_tesseract_single():
            response = detect_text_from_page_tesseract_single_thread(path_to_files)
        extract_text_tesseract_single()
    elif teserract_option == "2":
        def extract_text_tesseract_single():
            responsesingle = detect_text_from_page_tesseract_single_thread(path_to_files)
            responsemulti = detect_text_from_page_tesseract_multi_thread(path_to_files)
            table = PrettyTable()
            table.field_names = ["Type", "Total time (sec)"]
            print(f"---------------------difference------------------------------")
            table.add_row(["Single Thread", responsesingle["total_time"]])
            table.add_row(["Multi Thread", responsemulti])
            table.add_row(["Difference", responsesingle["total_time"] - responsemulti])
        # Print the table with a box around it
            print(table.get_string(border=True, padding_width=2))
            print(f"-------------------------------------------------------------")
        extract_text_tesseract_single()
elif option == "2":
    def extract_text_gcp():
        response = detect_text_from_page_google_vision(path_to_files)
        return response
    extract_text_gcp()