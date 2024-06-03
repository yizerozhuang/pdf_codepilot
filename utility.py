import os
import pypdf
import json
import subprocess
import webbrowser
import _thread

from PyPDF2 import PdfFileReader

from config import CONFIGURATION as conf

from pypdf.generic import RectangleObject
from pypdf import PageObject, Transformation
from pypdf._utils import CompressedTransformationMatrix

# def get_bluebeam_decode_result(input_byte):
#     result_byte = input_byte.decode("utf-8").split("\r\n1\r\n")
#     print()


#
# def flatten_the_pdf()


def convert_mm_to_pixel(input_length):
    return round(input_length * conf["mm_to_pixel"], 2)


def file_exists(file_dir):
    return os.path.exists(file_dir)

def read_json(json_dir):
    return json.load(open(json_dir))

def write_json(json_dir, json_dict):
    with open(json_dir, "w") as f:
        json_object=json.dumps(json_dict, indent=4)
        f.write(json_object)

def save_tk_to_json(app, json_dir):
    data_json = convert_to_json(app.data)
    write_json(json_dir, data_json)

def convert_to_json(obj):
    if isinstance(obj, list):
        return [convert_to_json(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_json(v) for k, v in obj.items()}
    else:
        return obj.get()

def load_json_to_tk(app, json_dir):
    data_json = read_json(json_dir)
    convert_to_data(data_json, app.data)

def convert_to_data(json, data):
    #todo: error to fix, return empty, might be python clear the stack after complate
    if isinstance(json, list):
        [convert_to_data(json[i], data[i]) for i in range(len(json))]
    elif isinstance(json, dict):
        [convert_to_data(json[key], data[key]) for key in json.keys()]
    else:
        data.set(json)

def is_float(input):
    try:
        float(input)
    except ValueError:
        return False
    return True


def open_folder(folder_dir):
    webbrowser.open(folder_dir)

def open_link_with_edge(link):
    edge_address = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    def open_link():
        subprocess.call([edge_address, link])
    _thread.start_new_thread(open_link, ())


def get_markup_xml_from_pdf(file_path, output_path):
    #assuming it's one page

    bluebeam_engine_dir = conf["bluebeam_engine_dir"]

    all_markup = return_makeup_by_page(file_path, 1)

    result_string_list = []

    for key in all_markup.keys():
        command = f"Open('{file_path}') MarkupCopy(1, '{key}')"
        result_byte = subprocess.check_output([bluebeam_engine_dir, command])
        result_string_list.append(result_byte.decode("utf-8"))

    with open(output_path, "w") as f:
        f.write("\n".join(result_string_list))

def get_paper_size(file_dir, page):
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]

    command = f"Open('{file_dir}') PageSize({page})"
    result_byte = subprocess.check_output([bluebeam_engine_dir, command])
    width = float(result_byte.decode("utf-8").split("\r\n")[1])
    height = float(result_byte.decode("utf-8").split("\r\n")[2])
    return width, height

def get_number_of_page(file_dir):
    reader = pypdf.PdfReader(file_dir)
    return len(reader.pages)
def get_sketch_name(project_dir):
    disk, folder_name = os.path.split(project_dir)
    project_name = folder_name.split('-', 1)[-1]
    return project_name + '-Mech Sketch.pdf'

def extract_disk_and_project_name(pdf_file):
    assert os.path.exists(pdf_file)
    dir_list = pdf_file.split('/')
    disk = dir_list[0]
    project_name = dir_list[1]
    filename = dir_list[-1]
    return disk, project_name, filename


def combine_pdf(input_file_list, output_file):
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]

    combine_pdfs = []
    for file in input_file_list:
        combine_pdfs.append('\'' + file + '\'')

    command = f"Combine({', '.join(combine_pdfs)}) Save('{output_file}') Close()"
    subprocess.check_output([bluebeam_engine_dir, command])



def flatten_pdf(input_file, output_file):
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]
    command= f"Open('{input_file}') Flatten(false) Save('{output_file}') Close()"
    subprocess.check_output([bluebeam_engine_dir, command])

# def rotate_page(input_page):
#     width = input_page.mediabox.width
#     height = input_page.mediabox.height
#     if height > width:
#         width, height = height, width
#     transformation = Transformation().rotate(360 - input_page.rotation)
#     input_page.add_transformation(transformation)
#     output_page = PageObject.create_blank_page(width=width, height=height)
#     output_page.merge_page(input_page)
#     return output_page

def resize_pdf(input_file, input_scale, input_size_x, input_size_y, output_scale, output_size_x, output_size_y, output_dir):

    # all_page_size = json.load(open("page_size.json"))

    # bluebeam_engine_dir = conf["bluebeam_engine_dir"]

    reader = pypdf.PdfReader(input_file)
    writer = pypdf.PdfWriter()

    # assert reader.pages[0].mediabox.lower_left == (0, 0)
    # pypdf.PdfWriter.flattened_pages = reader.pages

    # input_page_x = all_page_size[input_size]["width"]
    # input_page_y = all_page_size[input_size]["height"]
    #
    # output_page_x = all_page_size[output_size]["width"]
    # output_page_y = all_page_size[output_size]["height"]

    page_scale_x = float(output_size_x) / float(input_size_x)
    page_scale_y = float(output_size_y) / float(input_size_y)


    content_scale_x = (float(input_scale) / float(output_scale)) / page_scale_x
    content_scale_y = (float(input_scale) / float(output_scale)) / page_scale_y

    op = Transformation().scale(content_scale_x, content_scale_y)


    for page in reader.pages:
        #remove empty view point
        if "/VP" in page.keys():
            page.pop("/VP")
        # if page.rotation != 0:
        #     page = rotate_page(page)
        if page_scale_x != 1 or page_scale_y != 1:
            page.scale(page_scale_x, page_scale_y)

        if content_scale_x != 1 or content_scale_y != 1:
            page.add_transformation(op)
        writer.add_page(page)
    writer.write(output_dir)

    # pypdftk.fill_form(sketch_dir, out_file=sketch_dir, flatten=True)
    # command= f"Open('{output_dir}') Flatten(false) Close(true)"
    # subprocess.check_output([bluebeam_engine_dir, command])
    # flatten_pdf(output_dir, output_scale)

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


def replace_string(string, replacement):
    for key, value in replacement.items():
        string = string.replace(key, value)
    return string



def format_markup_input(input_data):
    return "{" +','.join([f'"{key}":"{value}"' for key, value in input_data.items()])+"}"

def bluebeam_markup_set(sketch_dir, page, markup_id, input_data):
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]
    input_data = format_markup_input(input_data)
    command= f"Open('{sketch_dir}') MarkupSet({page}, '{markup_id}', '{input_data}')  Save() Close()"
    subprocess.check_output([bluebeam_engine_dir, command])


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
    try:
        result_json = eval(string)
    except Exception as e:
        print(e)
        print(string)
    else:
        return result_json

# def get_rotation_matrix(degree):
#     assert degree in [0, 90, 180, 270]
#     if degree == 0:
#         return Transformation()
#     elif degree == 90:
#         return Transformation(ctm=(0, -1, 1, 0, 0, 0))





def align(sketch_dir):
    #bluebeam 72 points equal to 1 inches
    bluebeam_engine_dir = conf["bluebeam_engine_dir"]
    total_pages = get_number_of_page(sketch_dir)


    coordinate_list = []
    for i in range(total_pages):
        markups = return_makeup_by_page(sketch_dir, i+1)
        first_key = list(markups.keys())[0]
        coordinate_list.append({
                "markup_id": first_key,
                "x": float(markups[first_key]["x"]),
                "y": float(markups[first_key]["y"]),
                "width": float(markups[first_key]["width"]),
                "height": float(markups[first_key]["height"])
            }
        )
    reader = pypdf.PdfReader(sketch_dir)
    writer = pypdf.PdfWriter()

    # for page in reader.pages:
    #     if "/Annots" in page:
    #         for annot in page["/Annots"]:
    #             obj = annot.get_object()
    #             print()




    first_coordinate = coordinate_list[0]
    writer.add_page(reader.pages[0])

    for i in range(1, len(reader.pages)):
        page = reader.pages[i]
        translation_x = first_coordinate["x"] - coordinate_list[i]["x"]

        # bluebeam y-axis is reversed
        translation_y = - (first_coordinate["y"] - coordinate_list[i]["y"])
        # if page.rotation != 0:
        #     op = Transformation().rotate(-page.rotation)
        #     page.add_transformation(op)

        # op = get_rotation_matrix(page.rotation).translate(translation_x, translation_y)
        assert page.rotation in [0, 90, 180, 270]


        if page.rotation == 0:
            op = Transformation().translate(translation_x, translation_y)
        elif page.rotation == 90:
            op = Transformation().translate(- translation_y, translation_x)
        elif page.rotation == 180:
            op = Transformation().translate(- translation_x, - translation_y)
        else:
            op = Transformation().translate( translation_y, - translation_x)
        page.add_transformation(op)

        # if page.rotation != 0:
        #     op = Transformation().rotate(page.rotation)
        #     page.add_transformation(op)


        writer.add_page(page)
    writer.write(sketch_dir)


    for i in range(1, len(reader.pages)):
        bluebeam_markup_set(sketch_dir, i+1, coordinate_list[i]["markup_id"],{
                "x": first_coordinate["x"],
                "y": first_coordinate["y"]
                # "width": first_coordinate["width"],
                # "height": first_coordinate["height"],
            }
        )

def open_pdf_in_bluebeam(sketch_dir):
    # bluebeam_dir = conf["bluebeam_dir"]
    # subprocess.call([bluebeam_dir, sketch_dir])

    bluebeam_engine_dir = conf["bluebeam_engine_dir"]
    command= f"Open('{sketch_dir}') View() Close()"
    subprocess.check_output([bluebeam_engine_dir, command])
    # command = f"Open('test.pdf')  MarkupGetExList(1) Close()"


def format_to_xml(input_json):
    res = '<?xml version="1.0" encoding="us-ascii"?>'
    res += '<MarkupCopyItem>'
    res += '<Type>'
    res += input_json["Type"]
    res += '</Type>'
    res += '<Raw>'
    res += input_json["Raw"]
    res += '</Raw>'
    res += '</MarkupCopyItem>'
    return res
def add_tags(sketch_dir, markuptype, x, y, tag, level):
    # original point at lower left
    # x, y is the percentage of the tag comparing to the size of whole page



    bluebeam_engine_dir = conf["bluebeam_engine_dir"]

    # mark_up_template_dir = "T:\\00-Template-Do Not Modify\\00-Bridge template\\pdf\\markup.pdf"
    #
    # result_json = return_makeup_by_page("T:\\00-Template-Do Not Modify\\00-Bridge template\\pdf\\markup.pdf", 1)
    #
    # first_key = list(result_json.keys())[0]
    #
    # command = f"Open('{mark_up_template_dir}') MarkupCopy(1, '{first_key}')"
    #
    # first_key_xml = subprocess.check_output([bluebeam_engine_dir, command])

    # mark_up_xml_dir = r"C:\Users\Admin\Documents\GitHub\pdf_codepilot\sample_pdf\markup.xml"
    #
    # sample_output_dir = r"C:\Users\Admin\Documents\GitHub\pdf_codepilot\sample_pdf\sample_output.pdf"
    #
    # with open(mark_up_xml_dir, "r") as f:
    #     markup_xml = f.read()
    # markup_xml_string = markup_xml.replace("  ", "").replace("\n", "")
    #
    # command = f"Open('{sample_output_dir}') MarkupPaste(1, '{markup_xml_string}', 0, 0) Save() Close()"
    # result_bytes = subprocess.check_output([bluebeam_engine_dir, command])
    # markup_id = result_bytes.decode("utf-8").split("\n")[1].replace("\r", "")
    #
    # bluebeam_markup_set(sample_output_dir, 1, markup_id, {"comment": "123123123213213213213"})


    # command = f"Open('{mark_up_template_dir}') MarkupCopy(1, '{first_key}')"


    markup_dir = os.path.join(conf["database_dir"], "markup.json")
    markup_json = read_json(markup_dir)

    formated_xml = format_to_xml(markup_json[markuptype])

    total_pages = get_number_of_page(sketch_dir)
    reader = pypdf.PdfReader(sketch_dir)



    markup_paste_list = []
    for i, page in enumerate(reader.pages):

        label_x = page.mediabox.width * x
        label_y = page.mediabox.height * y


        assert page.rotation in [0, 90, 180, 270]

        # print(page.rotation)

        if page.rotation == 0:
            markup_paste_list.append(f"MarkupPaste({i+1}, '{formated_xml}', {label_x}, {label_y})")
        elif page.rotation == 90:
            markup_paste_list.append(f"MarkupPaste({i + 1}, '{formated_xml}', {page.mediabox.width-label_y}, {label_x})")
        elif page.rotation == 180:
            markup_paste_list.append(f"MarkupPaste({i + 1}, '{formated_xml}', {page.mediabox.width-label_x}, {page.mediabox.height-label_y})")
        else:
            markup_paste_list.append(f"MarkupPaste({i + 1}, '{formated_xml}', {label_y}, {page.mediabox.height-label_x})")


    command = f"Open('{sketch_dir}') " + " ".join(markup_paste_list) + " Save() Close()"
    new_markup_result = subprocess.check_output([bluebeam_engine_dir, command])
    new_markup_list = [markup_id.replace("1", "").replace("\r", "").replace("\n", "") for markup_id in new_markup_result.decode("utf-8").split("\r\n1\r\n")]\

    for i in range(total_pages):
        bluebeam_markup_set(sketch_dir, i+1, new_markup_list[i], {"comment": level[i].get().upper()+"\n"+tag})


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