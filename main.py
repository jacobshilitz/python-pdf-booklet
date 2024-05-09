import os
import sys
from pathlib import Path
import argparse
import pycpdflib

__version__ = '1.0.3'
__package_name__ = 'booklet'

INCHES_PER_POINT = 72
PAPER_SIZES = {
    'LTR': {'w': 11, 'h': 8.5},
    '11x17': {'w': 11, 'h': 17},
}

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    lib_path = Path(getattr(sys, '_MEIPASS', Path.cwd()))
    os.add_dll_directory(str(lib_path / "libcpdf"))
    pycpdflib.loadDLL("libpycpdf.dll")
else:
    print("This platform is not supported.")
    sys.exit(1)

def get_basename_file(file_path):
    base_name = os.path.basename(file_path)  # Returns 'filename.extension'
    file_name_without_extension = os.path.splitext(base_name)[0]  # Returns 'filename'
    return file_name_without_extension

def booklet_pdf(data):
    pdf_file = data['input_pdf']
    output_file = data['output_pdf'] if data['output_pdf'] else get_basename_file(pdf_file) + "_booklet.pdf"
    hp = data.get('hp', False)
    resize_only = data.get('resize_only', False)
    ltr = data.get('ltr', False)
    paper = data.get('paper', 'LTR')

    source_pdf = pycpdflib.fromFile(pdf_file, '')
    pdf_range = pycpdflib.all(source_pdf)

    pdf_size = pycpdflib.getMediaBox(source_pdf, 1)
    pdf_height = pdf_size[3]
    pdf_width = pdf_size[1]
    total_pages = pycpdflib.pages(source_pdf)

    # if it has crop we use the cropsize
    if pycpdflib.hasBox(source_pdf, 1, '/CropBox'):
        pdf_crop_size = pycpdflib.getCropBox(source_pdf, 1)

        pdf_crop_width = pdf_crop_size[1] - pdf_crop_size[0]
        pdf_crop_height = pdf_crop_size[3] - pdf_crop_size[2]

        print("Original PDF crop size w:", round(pdf_crop_width / INCHES_PER_POINT, 2), "h:",
              round(pdf_crop_height / INCHES_PER_POINT, 2))

        pdf_height = pdf_crop_height
        pdf_width = pdf_crop_width

    #     remove cropp age
    #     pycpdflib.getCropBox()

    print('Original PDF size w:', round(pdf_width / INCHES_PER_POINT, 2), 'h:', round(pdf_height / INCHES_PER_POINT, 2))

    paper_size = PAPER_SIZES.get(paper, False)

    if not paper_size:
        print("Invalid paper size")
        sys.exit(1)

    desired_width_in_inch = paper_size.get('w')
    desired_height_in_inch = paper_size.get('h')

    if not resize_only:
        #      rotate page size and split width in half
        if paper_size.get('h') > paper_size.get('w'):
            desired_width_in_inch = paper_size.get('h')
            desired_height_in_inch = paper_size.get('w')

        desired_width_in_inch = desired_width_in_inch / 2
    print("_______________")
    print('Desired width per page: ' + str(desired_width_in_inch))
    print('Desired height per page: ' + str(desired_height_in_inch))
    print("_______________")

    desired_width = desired_width_in_inch * INCHES_PER_POINT
    desired_height = desired_height_in_inch * INCHES_PER_POINT

    print("")

    height_scale = desired_height / pdf_height
    width_scale = desired_width / pdf_width

    # apply the scale
    pycpdflib.scalePages(source_pdf, pdf_range, width_scale, height_scale)

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

    if hp:
        print("hp mode is running")
        page_order = hp_sort(page_order)

    if not resize_only:
        source_pdf = pycpdflib.selectPages(source_pdf, page_order)

        pycpdflib.impose(source_pdf, 2, 1, False, False, (not ltr), False, False, False, False, False)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__package_name__, description='Convert pdf to booklet')
    parser.add_argument('input_pdf', type=str, help='Path to the input pdf file')
    parser.add_argument('output_pdf', type=str, help='Path to the output pdf file', nargs='?')
    parser.add_argument('--hp', help='HP mode', action='store_true')
    parser.add_argument('--ltr', help='left to right', action='store_true')
    parser.add_argument('--resize_only', help='just resize, no booklet', action='store_true')
    parser.add_argument('--paper', type=str, help='Specify paper size. Available options: LTR, 11x17',
                        choices=['LTR', '11x17'], default='LTR')

    args = parser.parse_args()
    data = vars(args)

    booklet_pdf(data)
