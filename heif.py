import os
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from datetime import datetime
import piexif
import re

register_heif_opener()

def heicToJpg(f, outpath):
    image = Image.open(f)
    image_exif = image.getexif()
    if not image_exif:
        return 

    exif = {
        ExifTags.TAGS[k]: v
        for k, v in image_exif.items()
        if k in ExifTags.TAGS
        and type(v) is not bytes
    }
    date = datetime.strptime(
        exif["DateTime"], "%Y:%m:%d %H:%M:%S"
    )

    exif_dict = piexif.load(image.info["exif"])
    exif_dict["0th"][
        piexif.ImageIFD.DateTime
    ] = date.strftime("%Y:%m:%d %H:%M:%S")
    exif_dict["0th"][
        piexif.ImageIFD.Orientation
    ] = 1

    exif_bytes = piexif.dump(exif_dict)
    image.save(outpath,
        "jpeg",
        exif=exif_bytes,
    )

