import fitz
from utils import *

# constants
WHITE = [1, 1, 1]
BLACK = [0, 0, 0]

# there are many examples at the bottom of the page

def fitz_open(file=0):
    if type(file) == fitz.fitz.Document:
        return file
    if not file:
        return fitz.open()
    file = add_extension(file, "pdf")
    return fitz.open(file)


def fitz_save(pdf, outpath, dir=0, openIt=1, incremental=0):
    if not outpath:
        outpath = pdf.metadata["title"]
    assert outpath
    outpath = add_extension(outpath, "pdf")
    if incremental:
        pdf.saveIncr()
    else:
        pdf.save(outpath)
    if openIt:
        ofile(outpath)




def white_bottom_page(pdf, page_num, horizontal, vertical):
    pdf = fitz_open(pdf)
    page = pdf[page_num - 1]
    di = page.rect
    args = []
    left = 0
    right = di.width
    top = 0
    bottom = di.height
    if is_function(horizontal):
        raise "`needs to be a func`"
    elif is_array(horizontal):
        left += horizontal[0]
        right -= horizontal[1]
    else:
        left += horizontal
        right -= horizontal

    if is_function(vertical):
        left, right = vertical(bottom)
    else:
        left += horizontal[0]
        right -= horizontal[1]

    # rect = fitz.Rect(left, top, right, bottom)
    rect = fitz.Rect(100, 600, 500, 800)
    # print(rect)
    # return
    # WHITE = BLACK
    page.draw_rect(rect, color=WHITE, fill=WHITE, width=1)
    return pdf



def white_bottom_footer(pdf, bottom = 0, left = 0, top = 0, right = 0, skip = []):
    def white(page):
        args = [
            left, # starts at the left
            page.rect.height - bottom, # bottom offset
            page.rect.width - right, # distance from right
            page.rect.height, # all the way to the bottom
        ]
        rect = fitz.Rect(*args)
        page.draw_rect(rect, color=WHITE, fill=WHITE, width=1)

    pdf = fitz_open(pdf)
    for i, page in enumerate(pdf):
        if i + 1 in skip:
            continue
        white(page)

    return pdf


def get_page_dimensions(pdf_path, page_number = 1):
    page_number = page_number - 1
    document = fitz_open(pdf_path)

    page_dimensions = document[0].rect
    width = page_dimensions.width
    height = page_dimensions.height
    print(printf("width: $width, height: $height"))

def delete_page_n(pdf, n):
    pdf = fitz_open(pdf)
    pdf.delete_page(n - 1)
    return pdf 

def extract_pdf_slice(file, a = 0, b = 0, outpath = test_dot_pdf):
    if not b:
        b = a
    a -= 1
    b -= 1
    document = fitz_open(file)
    new_doc = fitz.open()
    new_doc.insert_pdf(document, from_page=a, to_page=b)
    fitz_save(new_doc, outpath)

def change_pdf_title(pdf, new_title):
    pdf = fitz_open(pdf)
    metadata = pdf.metadata

    metadata['title'] = new_title
    pdf.set_metadata(metadata)
    return pdf

# example
# get_page_dimensions(test_dot_pdf)

# example
# file = "/mnt/chromeos/GoogleDrive/MyDrive/Chess Workbook (Part 1) [Advertisement].pdf"
# extract_pdf_slice(file, 1, 1)
# note: extracts the first page of the pdf
# extract_pdf_slice(file, 3, 6)
# extracts pages 3,4,5,6.



# example
# file = test_dot_pdf
# pdf = white_bottom_page(file, page_num = 1, horizontal = 100, vertical = lambda bottom: (bottom - 150, bottom - 50))
# this doesnt work too well
# fitz_save(pdf, clip_dot_pdf)
# note: clears out the bottom of the page



# example: editing the chess workbook
# file = "/mnt/chromeos/GoogleDrive/MyDrive/Chess Workbook (Part 1) [Advertisement].pdf"
# pdf = fitz_open(file)
# pdf = white_bottom_footer(pdf, skip = [1], bottom = 50, left = 150, right = 150)
# pdf = white_bottom_page(pdf, page_num = 1, horizontal = 100, vertical = lambda bottom: (bottom - 150, bottom - 50))
# pdf = delete_page_n(pdf, 2)
# pdf = change_pdf_title(pdf, "Chess Program Intro")
# fitz_save(pdf, test_dot_pdf)
# takes the chess book, removes the bottom of page margin
# alters the front page a bit
# renames the pdf
