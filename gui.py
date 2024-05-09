from tkinter import Tk, Label, Button, Entry, StringVar, Checkbutton, BooleanVar, filedialog, OptionMenu
from threading import Thread
from main import booklet_pdf, __version__, PAPER_SIZES


class GUI:



    def __init__(self, window):
        self.window = window
        window.geometry('500x250')

        window.title("Booklet PDF GUI " + __version__)

        padding = 2
        margin = 10
        entry_width = 50

        self.input_pdf_str = StringVar()
        Label(window, text="Input PDF:").grid(row=0, column=0, sticky="W", padx=margin, pady=padding)
        Entry(window, textvariable=self.input_pdf_str, width=entry_width).grid(row=0, column=1, padx=margin,
                                                                               pady=padding)
        Button(window, text='Browse', command=self.load_input_file).grid(row=0, column=2, padx=margin, pady=padding)

        self.output_pdf_str = StringVar()
        Label(window, text="Output PDF:").grid(row=1, column=0, sticky="W", padx=margin, pady=padding)
        Entry(window, textvariable=self.output_pdf_str, width=entry_width).grid(row=1, column=1, padx=margin,
                                                                                pady=padding)
        Button(window, text='Browse', command=self.save_output_file).grid(row=1, column=2, padx=margin, pady=padding)

        self.hp_str = BooleanVar()
        Checkbutton(window, text="HP mode", var=self.hp_str).grid(row=2, column=0, columnspan=3, padx=margin,
                                                                  pady=padding, sticky="EW")

        self.ltr_str = BooleanVar()
        Checkbutton(window, text="LTR mode", var=self.ltr_str).grid(row=3, column=0, columnspan=3, padx=margin,
                                                                    pady=padding, sticky="EW")

        self.resize_only_str = BooleanVar()
        Checkbutton(window, text="Resize only", var=self.resize_only_str).grid(row=4, column=0, columnspan=3,

                                                                               padx=margin, pady=padding, sticky="EW")
        paper_options = list(PAPER_SIZES.keys())

        self.paper_option = StringVar()
        self.paper_option.set(paper_options[0])

        OptionMenu(window, self.paper_option, *paper_options).grid(row=5, column=1, columnspan=1, padx=margin, pady=padding, sticky="EW")

        Button(window, text="Generate Booklet PDF", command=self.generate_pdf).grid(row=6, column=1, padx=margin,
                                                                                    pady=padding)

    def generate_pdf(self):

        data = {
            'input_pdf': self.input_pdf_str.get(),
            'output_pdf': self.output_pdf_str.get(),
            'hp': self.hp_str.get(),
            'ltr': self.ltr_str.get(),
            'resize_only': self.resize_only_str.get(),
            'paper': self.paper_option.get()
        }

        def task():
            try:
                self.status_label = Label(self.window, text="Processing... Please wait.")
                self.status_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="EW")

                booklet_pdf(data)
                self.status_label.config(text="Success: Booklet PDF successfully generated")
            except Exception as e:
                self.status_label.config(text=str(e))

        thread = Thread(target=task)
        thread.start()

    def load_input_file(self):
        file_name = filedialog.askopenfilename(title="Open Input PDF",
                                               filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*")))
        if file_name:
            self.input_pdf_str.set(file_name)

    def save_output_file(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Output PDF",
                                                 filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*")))
        if file_name:
            self.output_pdf_str.set(file_name)


def run_gui():
    root = Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    run_gui()
