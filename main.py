import time
from ctypes import windll, Structure, c_long, byref
import ctypes
from tkinter import Tk, Canvas, Text
import tkinter as tk
from functools import partial
import importlib
import pathlib

import cv2
import mss
import numpy
import pytesseract

# TODO: make root.geometry depend on this
from get_monitors import monitor_areas
import glob, importlib, os, pathlib, sys

RES_FONT = 'Helvetica 10'
RES_FONT_BOLD = RES_FONT + ' bold'

def get_all_scripts() -> dict:
    path = pathlib.Path(__file__).parent.resolve()
    MODULE_DIR = str(path / 'scripts')
    sys.path.append(MODULE_DIR)

    py_files = glob.glob(os.path.join(MODULE_DIR, '*.py'))

    scripts_data = {}
    for py_file in py_files:
        module_name = pathlib.Path(py_file).stem
        module = importlib.import_module(module_name)
        scripts_data[module.__name__] = module
    
    return scripts_data

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
main_scripts = get_all_scripts()

def display_result(result):
    ## Add button to view original text
    headers = []

    for row in result:
        headers += row.keys()

    headers = list(dict.fromkeys(headers))

    root = tk.Tk()
    root.title("Results")

    frame = tk.Frame(root, padx=20, pady=10)
    frame.pack()

    for i, value in enumerate(headers):
        entry = tk.Entry(frame, justify="center", font=RES_FONT_BOLD)
        entry.grid(row=1, column=i)
        entry.insert(tk.END, value)
        entry["state"] = tk.DISABLED


    for n, row in enumerate(result):
        unused_columns = list(range(len(headers)))
        
        for key, value in row.items():
            index = headers.index(key)
            unused_columns.remove(index)
            entry = tk.Entry(frame, justify="center", font=RES_FONT)
            entry.grid(row=n+2, column=index)
            entry.insert(tk.END, value)
            entry["state"] = tk.DISABLED

        for unused_index in unused_columns:
            entry = tk.Entry(frame, justify="center", font=RES_FONT)
            entry.grid(row=n+2, column=unused_index)
            entry["state"] = tk.DISABLED
            
    root.mainloop()

def run_script(var, textarea):
    text = textarea.get("1.0",'end-1c')
    global main_scripts
    module_name = var.get()
    result = main_scripts.get(module_name).Main(text).run()
    display_result(result)

def new_window(text):
    new_root = Tk()
    new_root.title("Massalyzer")
    new_root.resizable(False, False)
    main_frame = tk.Frame(master=new_root)
    main_frame.pack(padx=5, pady=10)
    textarea = Text(main_frame)
    textarea.grid(row=1, column=1, padx=10)
    textarea.insert(tk.END, text)
    btns_frame = tk.Frame(master=main_frame, relief=tk.RAISED)
    btns_frame.grid(row=1, column=2, sticky="n", padx=5)
    button = tk.Button(btns_frame, text="Scripts", padx=14)
    button['state'] = "disabled"
    button.pack(pady=7)
    var = tk.StringVar()
    global main_scripts
    scripts_frame = tk.Frame(master=btns_frame)
    scripts_frame.pack(pady=20)

    for script_name in main_scripts.keys():
        radio_button = tk.Radiobutton(scripts_frame, text=script_name, variable=var, value=script_name)
        radio_button.pack(anchor="w")
    radio_button.select()

    run = tk.Button(btns_frame, text="Run", padx=20, command=lambda: run_script(var, textarea))
    run.pack(pady=10)
    new_root.mainloop()
    
def screenshot(x1, y1, x2, y2):
    mon = {'top': y1 if y1 < y2 else y2, 'left': x1 if x1 < x2 else x2, 'width': abs(x2 - x1), 'height': abs(y2 - y1)}
    with mss.mss() as sct:
        im = numpy.array(sct.grab(mon))
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(image=im)
        new_window(text)

        # cv2.imshow('Image', im)
        # # Press "q" to quit
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        # time.sleep(19)

def img_to_string(image):
    text = pytesseract.image_to_string(image=image, config='digits')
    return text

# if __name__ == "__main__":
#     root = Tk()

#     root.geometry("5000x5000")
#     root.attributes('-alpha', 0.3)
#     root.overrideredirect(True)
#     canvas = Canvas(root, width=5000, height=5000)
#     canvas.pack()

#     # small hack to save the inital place of the cursor (bcz event B1 motion keeps repeating the function each time)
#     app_data = {"first_call": True, "x1": 0, "y1": 0}

#     def drag_handler(event):
#         # define global variables 
#         global app_data, root, canvas

#         # delete rectangle if any were created by previous call
#         canvas.delete("rect")

#         if app_data['first_call']:
#             app_data["x1"] = root.winfo_pointerx()
#             app_data["y1"] = root.winfo_pointery()

#         time.sleep(0.01)
#         app_data['x2'] = root.winfo_pointerx()
#         app_data['y2'] = root.winfo_pointery()

#         canvas.create_rectangle(app_data["x1"], app_data["y1"], app_data['x2'], app_data['y2'], fill='red', tags="rect")
#         app_data['first_call'] = False

#     def stop_scrolling(event):
#         global app_data, root
#         root.destroy()
#         if app_data.get('x2', None):
#             screenshot(app_data['x1'], app_data['y1'], app_data['x2'], app_data['y2'])

#     def close(event):
#         global root
#         root.destroy()

#     canvas.bind("<B1-Motion>", drag_handler)
#     canvas.bind('<ButtonRelease-1>', stop_scrolling)
#     root.bind("<Escape>", close)
#     root.mainloop()

if __name__ == "__main__":
    text = """
    36.190.55.235
87.193.92.28
159.47.150.72
115.73.93.242
182.138.10.219
29.117.52.108
139.106.150.81
195.18.71.195
233.32.23.197
232.217.166.149

asdasd
sadsad
xcz
xc
xzc
zx
czx
c
"""
    module_name = "IP"
    result = main_scripts.get(module_name).Main(text).run()
    display_result(result)