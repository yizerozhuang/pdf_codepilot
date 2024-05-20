import os
import pypdf
import json
import pypdftk
import subprocess

from config import CONFIGURATION as conf


#
# def flatten_the_pdf()

def extract_disk_and_project_name(pdf_file):
    assert os.path.exists(pdf_file)
    dir_list = pdf_file.split('/')
    disk = dir_list[0]
    project_name = dir_list[1]
    filename = dir_list[-1]
    return disk, project_name, filename

def flatten_and_resize_pdf(input_file, input_scale, input_size, output_scale, output_size, sketch_dir):
    assert os.path.exists(input_file)

    all_page_size = json.load(open("page_size.json"))

    bluebeam_engine_dir = conf["bluebeam_engine_dir"]

    reader = pypdf.PdfReader(input_file)
    writer = pypdf.PdfWriter()

    # pypdf.PdfWriter.flattened_pages = reader.pages

    input_page_x = all_page_size[input_size]["width"]
    input_page_y = all_page_size[input_size]["height"]

    output_page_x = all_page_size[output_size]["width"]
    output_page_y = all_page_size[output_size]["height"]

    page_scale_x = output_page_x / input_page_x
    page_scale_y = output_page_y / input_page_y


    content_scale_x = (float(input_scale) / float(output_scale)) / page_scale_x
    content_scale_y = (float(input_scale) / float(output_scale)) / page_scale_y
    op = pypdf.Transformation().scale(content_scale_x, content_scale_y)


    for page in reader.pages:
        page.scale(page_scale_x, page_scale_y)
        page.add_transformation(op)
        writer.add_page(page)
    writer.write(sketch_dir)

    # pypdftk.fill_form(sketch_dir, out_file=sketch_dir, flatten=True)
    command= f"Open('{sketch_dir}')  Flatten(false) Close(true)"
    subprocess.check_output([bluebeam_engine_dir, command])
    print("Done")
    return

def grays_scale_pdf(sketch_dir):
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]
    command= f"Open('{sketch_dir}')  ColorProcess('black','white') Close(true)"
    subprocess.check_output([bluebeam_engine_dir, command])
    print("Done")
    return

def compress(sketch_dir):
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]
    new_sketch_dir = sketch_dir[:-4]+"_compressed.pdf"
    command= f"Open('{sketch_dir}') ReduceFileSize() Save('{new_sketch_dir}') Close()"
    subprocess.check_output([bluebeam_engine_dir, command])
    print("Done")
    return


def replace_string(string, replacement):
    for key, value in replacement.items():
        string = string.replace(key, value)
    return string
def return_makeup_by_page(file_dir, i):
    command = f"Open('{file_dir}')  MarkupGetExList({i}) Close()"
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]

    result_bytes = subprocess.check_output([bluebeam_engine_dir, command])
    result_text = result_bytes.decode("utf-8").split("\n")[1]
    replacement = {
        "|'": "'",
        "'{": "{",
        "}'": "}",
        "||": "\\",
        "'True'": "True",
        "'False'": "False",
        "'None'": "None"
    }
    string = replace_string(result_text, replacement)
    result_json = eval(string)
    return result_json

def align(sketch_dir):
    #bluebeam 72 points equal to 1 inches
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]
    command = f"Open('{sketch_dir}') PageCount() Close(true)"
    result_bytes = subprocess.check_output([bluebeam_engine_dir, command])
    total = result_bytes.decode("utf-8")[0]

    coordinate_list = []
    for i in range(int(total)):
        markups = return_makeup_by_page(sketch_dir, i+1)
        first_key = list(markups.keys())[0]
        coordinate_list.append({
                "x":float(markups[first_key]["x"]),
                "y":float(markups[first_key]["y"]),
                "width":float(markups[first_key]["width"]),
                "height":float(markups[first_key]["height"])
            }
        )
    reader = pypdf.PdfReader(sketch_dir)
    writer = pypdf.PdfWriter()

    first_coordinate = coordinate_list[0]
    writer.add_page(reader.pages[0])

    for i in range(1, len(reader.pages)):
        page = reader.pages[i]
        translation_x = first_coordinate["x"] - coordinate_list[i]["x"]
        translation_y = first_coordinate["y"] - coordinate_list[i]["y"]
        op = pypdf.Transformation().translate(translation_y, translation_x)
        page.add_transformation(op)
        writer.add_page(page)

    writer.write(sketch_dir)

    print("Done")


def open_pdf_in_bluebeam(sketch_dir):
    bluebeam_dir = conf["bluebeam_dir"]
    subprocess.call([bluebeam_dir, sketch_dir])
    # command = f"Open('test.pdf')  MarkupGetExList(1) Close()"



#
# combine_pdfs = []
# for file in os.listdir("."):
#     if file.endswith(".pdf"):
#         combine_pdfs.append('\''+file+'\'')
#
# # command = f"Combine({', '.join(combine_pdfs)}) Flatten() Save('{file_name}') View() Close()"
# # command = f"Open('{combine_pdfs[0]}') Save('123.pdf') Close()"
# # command = "Open('20240509-combined.pdf') FormExport('123.fdf') Close()"
# # command = f"Open('test.pdf') ColumnsExport('columns.xml') Close()"
# # command = f"Open('test.pdf')  MarkupGetExList(1) Close()"
# return_makeup_by_page("test.pdf", 2)