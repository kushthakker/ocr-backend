import os
from utils import *
from pydantic import BaseModel
import json

output_dir = "output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
    print(f"Directory '{output_dir}' created.")
else:
    print(f"Directory '{output_dir}' already exists.")
convert_to_images("./12100010_f1.pdf")

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
            json_data = json.dumps(response)
            file_path = "./output_json.json"
            with open(file_path, "w") as file:
                file.write(json_data)
            print("JSON file created successfully.")
            return response
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
            page_text = []
            for p in responsesingle["pages"]:
                page_text.append(p['page_text'])

            response = {
                "single_thread_time": responsesingle["total_time"],
                "multi_thread_time": responsemulti,
                "page_text": page_text
            }
         
            json_data = json.dumps(response)
            file_path = "./output_json.json"
            with open(file_path, "w") as file:
                file.write(json_data)
            print("JSON file created successfully.")
            return response
        extract_text_tesseract_single()
elif option == "2":
    def extract_text_gcp():
        response = detect_text_from_page_google_vision(path_to_files)
        json_data = json.dumps(response)
        file_path = "./output_json.json"
        with open(file_path, "w") as file:
         file.write(json_data)
        print("JSON file created successfully.")
        return response
    extract_text_gcp()