# PDF Booklet Generator

This is a Python executable script that converts a standard PDF file into a PDF booklet. The booklet generator uses the `pycpdflib` library to manipulate the PDF pages.

## User Guide

The PDF booklet generator can be executed directly without the need for any installations or environment setups. Here is how you can use the program:

### Usage

The executable takes as input the paths to the input and output files. It has options for HP mode, left-to-right ordering, and just resizing without creating a booklet.

Run the executable in your terminal/command line as follows:

```shell
.booking input_pdf_path output_pdf_path [--hp] [--ltr] [--resize_only]
```

### Command Line Arguments

All command line arguments are required except for those in square brackets:

- `input_pdf`: Path to the input PDF file.
- `output_pdf`: Path to where the output PDF file will be saved.
- `--hp`: This option enables HP mode, which changes the page ordering.
- `--ltr`: This option specifies left-to-right page ordering for the booklet.
- `--resize_only`: This option resizes the pages without creating a booklet.

## Developer Guide

If you are a developer and want to further modify or contribute to this project, here are the instructions on the project setup:

### Prerequisites

You will need the following on your system:

- Python 3.11.6 or higher
- The `pycpdflib` library

### Installation

To install the necessary library, you can use pip:

```shell
pip install pycpdflib
```

### Building the Executable

The PyInstaller library can be used to package the Python script into an executable. If not already installed, you can install it using pip:

```shell
pip install pyinstaller
```

Then you can generate the executable with the following command:

```shell
pyinstaller --onefile filename.py
```

Replace `filename.py` with the actual name of the script file you want to convert to executable.

The `--onefile` option tells PyInstaller to create a single executable file. If you prefer to have a bundled directory (containing an executable along with other files that your program needs), you can leave out the `--onefile` option.

Remember to replace `filename.py` with your actual Python script name in the command. The generated executable will be located in the `dist` directory.

**Notes:**

- This booklet creator currently supports Windows (32-bit and 64-bit) and Cygwin platforms.
- HP mode and other options are under development and may not be fully functional.

Please make sure to take a backup of your original file before using this tool as the resizing algorithm could distort the aspect ratio of the original PDF.