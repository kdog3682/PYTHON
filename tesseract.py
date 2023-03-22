from PIL import Image
import pytesseract

def tesseractExtractText(imageFile):
    return pytesseract.image_to_string(Image.open(imageFile))
