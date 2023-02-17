
def downloadImage(url, name):
    from requests import get
    r = get(url)

a = 'asdf'
asdfasdfsd = 'asdf'
#chdir(rootdir)
#shutil.move('VIM & SH', 'VIM')
#printdir(rootdir)

#pprint(mostRecentFileGroups(rootdir + 'SVG', minutes=5))

def downloadImage(url, name):
    from requests import get
    r = get(url)
    if r.status_code == 200:
        with open(name,'wb') as f:
            f.write(r.content)
            print('Image sucessfully Downloaded: ',name)
            return name
    else:
        print('Image Couldn\'t be retreived', name) 






#SystemCommand('npm update')
#SystemCommand('git show --name-only')
#SystemCommand('git add .\ngit show --name-only')
#SystemCommand('git rev-list --all --count') # 34 commits
#SystemCommand('git shortlog -s')
#ff(text='g4stud', js=1)
#print(tail(pydir))
#mfile('vue-directives.js', 'vue-utils.js')


#import PyPDF2
#from PyPDF2.pdf import ContentStream, PageObject, PDFTextObject

def get_color_region_coordinates(pdf_path):
    color_regions = []
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            content = page.getContents()

            if isinstance(content, ContentStream):
                content = content.stream

            if not isinstance(content, PDFTextObject):
                color_region = None
                for operands, operator in PyPDF2.pdf.PdfContentReader(content).operations:
                    if operator == 'rg':
                        # This is a color setting operator.
                        if color_region is None:
                            color_region = [operands[-2], operands[-1]]
                        else:
                            color_region.extend([operands[-2], operands[-1]])
                    elif operator == 'h' and color_region is not None:
                        # This is a path-closing operator.
                        color_regions.append(color_region)
                        color_region = None

                if color_region is not None:
                    # If there is a color region that hasn't been closed, add it to the list of regions.
                    color_regions.append(color_region)

    return color_regions

#print(get_color_region_coordinates('/mnt/chromeos/MyFiles/Downloads/test.pdf'))


#import fitz
from pprint import pprint
def get_nonblack_color_regions(pdf_path):
    color_regions = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap()
            img = pix.tobytes("np")
            pprint(img)
            return 
            has_color = (img[:,:,0] != 0) | (img[:,:,1] != 0) | (img[:,:,2] != 0)
            # Find the bounding box of the non-black region.
            ys, xs = has_color.nonzero()
            if len(xs) > 0 and len(ys) > 0:
                x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
                color_regions.append((page.number, (x0, y0, x1, y1)))
    return color_regions


import pikepdf

def get_nonblack_color_regions(pdf_path):
    color_regions = []
    with pikepdf.open(pdf_path) as doc:
        for page_num, page in enumerate(doc.pages):
            if page['/Resources'] is not None and '/XObject' in page['/Resources']:
                for xobject_name, xobject_stream in page['/Resources']['/XObject'].items():
                    if xobject_stream.Filter == '/FlateDecode':
                        print(xobject_stream['/FlateDecode'])
                        return 
                        pix = xobject_stream.FlateDecode()
                        img = pix.to_ndarray()
                        has_color = (img[:,:,0] != 0) | (img[:,:,1] != 0) | (img[:,:,2] != 0)
                        ys, xs = has_color.nonzero()
                        if len(xs) > 0 and len(ys) > 0:
                            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
                            color_regions.append((page_num, xobject_name, (x0, y0, x1, y1)))
    return color_regions

#print(get_nonblack_color_regions('/mnt/chromeos/MyFiles/Downloads/Hello Kitty Back to School coloring page _ Free Printable Coloring Pages.pdf'))
