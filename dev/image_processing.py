import piexif
from PIL import Image

def exif_to_tag(exif_dict):
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    exif_tag_dict['thumbnail'] = thumbnail.decode("ISO-8859-1")

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode("ISO-8859-1")

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict

def extract_GPS_data_from_image(input_image_file):
    im = Image.open(input_image_file)
    exif_dict = piexif.load(im.info.get('exif'))
    image_GPS_data = exif_to_tag(exif_dict)['GPS']
    return image_GPS_data

def DMS_to_DD(degree, minute, second):
    return degree + (minute/60) + (second/3600)

def extract_coordinates_and_bearing_from_GPS_data(inputDict):
    latitudes = inputDict.get("GPSLatitude")

    if latitudes is None:
        inputLatDeg = 0
        inputLatMin = 0
        inputLatSec = 0
    else:
        inputLatDeg = latitudes[0][0]
        inputLatMin = latitudes[1][0]
        inputLatSec = latitudes[2][0]/1000

    if inputDict.get("GPSLatitudeRef") == 'S':
        latHemisphere = -1
    else:
        latHemisphere = 1

    outputLat = DMS_to_DD(inputLatDeg, inputLatMin, inputLatSec) * latHemisphere

    longitudes = inputDict.get("GPSLongitude")

    if longitudes is None:
        inputLonDeg = 0
        inputLonMin = 0
        inputLonSec = 0
    else:
        inputLonDeg = longitudes[0][0]
        inputLonMin = longitudes[1][0]
        inputLonSec = longitudes[2][0]/1000

    if inputDict.get("GPSLongitudeRef") == 'W':
        lonHemisphere = -1
    else:
        lonHemisphere = 1

    outputLon = DMS_to_DD(inputLonDeg, inputLonMin, inputLonSec) * lonHemisphere

    inputBearing = inputDict.get('GPSImgDirection')

    if inputBearing[1] !=0:
        outputBearing = inputBearing[0]/inputBearing[1]
    else:
        outputBearing = 0

    return outputLat, outputLon, outputBearing