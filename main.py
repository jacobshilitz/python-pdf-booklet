import os
import sys
from pathlib import Path
import argparse

import pycpdflib

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    lib_path = Path(getattr(sys, '_MEIPASS', Path.cwd()))
    os.add_dll_directory(str(lib_path / "libcpdf"))
    pycpdflib.loadDLL("libpycpdf.dll")
else:
    print("This platform is not supported.")
    sys.exit(1)


def booklet_pdf(args):
    pdf_file = args.input_pdf
    output_file = args.output_pdf

    source_pdf = pycpdflib.fromFile(pdf_file, '')
    pdf_range = pycpdflib.all(source_pdf)
    pdf_size = pycpdflib.getMediaBox(source_pdf, 1)
    total_pages = pycpdflib.pages(source_pdf)

    pdf_height = pdf_size[3]
    pdf_width = pdf_size[1]

    letter_x_size = 5.5 * 72
    letter_y_size = 8.5 * 72

    x_scale = letter_y_size / pdf_height
    y_scale = letter_x_size / pdf_width

    pycpdflib.scalePages(source_pdf, pdf_range, y_scale, x_scale)

    remainder = total_pages % 4
    blank_pages = 0 if remainder == 0 else 4 - remainder

    for blankPage in range(total_pages, total_pages + blank_pages):
        pycpdflib.padAfter(source_pdf, [blankPage])

    pages = list(range(1, (total_pages + blank_pages + 1)))
    page_order = []

    while pages:
        page_order.append(pages.pop())
        page_order.append(pages.pop(0))
        page_order.append(pages.pop(0))
        page_order.append(pages.pop())

    if args.hp:
        print("hp mode is running")
        page_order = hp_sort(page_order)

    if not args.resize_only:
        source_pdf = pycpdflib.selectPages(source_pdf, page_order)

        pycpdflib.impose(source_pdf, 2, 1, False, False, (not args.ltr), False, False, False, False, False)

    pycpdflib.toFile(source_pdf, output_file, False, False)

    print("Resized PDF to", output_file)

def hp_sort(arr):
    # splitting list into sub-lists of 4 elements
    sub_lists = [arr[i:i + 4] for i in range(0, len(arr), 4)]

    # reversing order of sub-lists
    sub_lists = sub_lists[::-1]

    # flattening list of sub-lists into one list
    flipped_arr = [item for sublist in sub_lists for item in sublist]

    return flipped_arr


parser = argparse.ArgumentParser(description='Convert pdf to booklet')
parser.add_argument('input_pdf', type=str, help='Path to the input pdf file')
parser.add_argument('output_pdf', type=str, help='Path to the output pdf file')
parser.add_argument('--hp', help='HP mode', action='store_true')
parser.add_argument('--ltr', help='left to right', action='store_true')
parser.add_argument('--resize_only', help='just resize, no booklet', action='store_true')

args = parser.parse_args()

booklet_pdf(args)
