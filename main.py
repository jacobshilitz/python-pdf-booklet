import os
import sys
from pathlib import Path

import pycpdflib

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    lib_path = Path(getattr(sys, '_MEIPASS', Path.cwd()))
    os.add_dll_directory(str(lib_path / "libcpdf"))
    pycpdflib.loadDLL("libpycpdf.dll")
else:
    print("This platform is not supported.")
    sys.exit(1)


def booklet_pdf(pdf_file, output_file):
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

    test_pdf = pycpdflib.selectPages(source_pdf, page_order)
    pycpdflib.impose(test_pdf, 2, 1, False, False, False, False, False, False, False, False)

    pycpdflib.toFile(test_pdf, output_file, False, False)

    print("Resized PDF to", output_file)


if len(sys.argv) > 1:
    input_path = sys.argv[1]
    output_path = sys.argv[2]
else:
    print("Usage: <input_path> <output_path>")
    sys.exit(1)

booklet_pdf(input_path, output_path)
