######### helpers.py #########

"""
File Name: helpers.py
Developer(s): Tyler Richman (tyler.richman@erg.com), Mark Fowler (mark.fowler@erg.com)
Last Update: 01/21/2025
Description: 
"""

def file_select():
    root = tk.Tk()
    filenames = askopenfilenames()
    root.destroy()
    return filenames

def exif_to_tag(exif_dict):
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict

def dict_extract(inputFile):
    im = Image.open(inputFile)
    exif_dict = piexif.load(im.info.get('exif'))
    exif_dict = exif_to_tag(exif_dict)
    return(exif_dict)

def decimal_degree(degree, minute, second):
    value = degree + (minute/60) + (second/3600)
    return value

def exif_coordinates(inputDict):
    latitudes = inputDict['GPS'].get("GPSLatitude")
    if latitudes is None:
        inputLatDeg = 0
        inputLatMin = 0
        inputLatSec = 0
    else:
        inputLatDeg = latitudes[0][0]
        inputLatMin = latitudes[1][0]
        inputLatSec = latitudes[2][0]/1000
    if inputDict['GPS'].get("GPSLatitudeRef") == 'S':
        latHemisphere = -1
    else:
        latHemisphere = 1
    outputLat = decimal_degree(inputLatDeg,inputLatMin,inputLatSec) *latHemisphere
    longitudes = inputDict['GPS'].get("GPSLongitude")
    if longitudes is None:
        inputLonDeg = 0
        inputLonMin = 0
        inputLonSec = 0
    else:
        inputLonDeg = longitudes[0][0]
        inputLonMin = longitudes[1][0]
        inputLonSec = longitudes[2][0]/1000
    if inputDict['GPS'].get("GPSLongitudeRef") == 'W':
        lonHemisphere = -1
    else:
        lonHemisphere = 1
    outputLon = decimal_degree(inputLonDeg,inputLonMin,inputLonSec) *lonHemisphere
    inputBearing = inputDict['GPS'].get('GPSImgDirection')
    if inputBearing[1] !=0:
        outputBearing = inputBearing[0]/inputBearing[1]
    else:
        outputBearing = 0
    return (outputLat,outputLon,outputBearing)
