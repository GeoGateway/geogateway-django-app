import io
import json
import subprocess
import zipfile
import csv


import requests
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.apps import apps
from airavata_django_portal_sdk import user_storage

# GNSS service url
GpsServiceUrl = "https://data.geo-gateway.org/gpsservice/kml?"
KmlPrefix = "https://data.geo-gateway.org/static"

# UAVSAR service url
wmsColorUrl = 'https://data.geo-gateway.org/color/InSAR/wms?'
wmsUrl = 'https://data.geo-gateway.org/color/highres/wms?'
losQueryUrl = 'https://data.geo-gateway.org/los/profile?dem=True&image=uid'

WoForecastUrl = 'http://www.openhazards.com/Tools/kml/wo-forecast.kmz'
CaForecastUrl = 'http://www.openhazards.com/Tools/kml/ca-forecast.kmz'

GdacsUrl = 'https://www.gdacs.org/xml/gdacsEQ.geojson'
NowcastUrl = "http://gf8.ucs.indiana.edu:8000/seismicityservice/plot?"

uavsarJsonUrl = 'http://gf2.ucs.indiana.edu/quaketables/uavsar/search?geometry='
geoServerUrl='http://gf2.ucs.indiana.edu/quaketables/uavsar/search?searchstring='


def gps_service(request):
    if request.method == 'GET':
        # more efficient way of getting request params?
        # getting request params from GET in GNSS.vue
        payload = {
            "function": request.GET.get("function"),  # .GET.get("function"),
            "lat": request.GET.get("lat"),
            "lon": request.GET.get("lon"),
            "width": request.GET.get("width"),
            "height": request.GET.get("height"),
            "epoch": request.GET.get("epoch"),
            "epoch1": request.GET.get("epoch1"),
            "epoch2": request.GET.get("epoch2"),
            "scale": request.GET.get("scale"),
            "ref": request.GET.get("ref"),
            "ct": request.GET.get("ct"),
            "pt": request.GET.get("pt"),
            "dwin1": request.GET.get("dwin1"),
            "dwin2": request.GET.get("dwin2"),
            "prefix": request.GET.get("prefix"),
            "mon": request.GET.get("mon"),
            "eon": request.GET.get("eon"),
            "vabs": request.GET.get("vabs"),
            "analysisCenter": request.GET.get("analysisCenter")}
        data = requests.get(GpsServiceUrl, params=payload)
        responseData = HttpResponse(data)
        return responseData


def get_gnss_kml(request):
    if request.method == 'GET':
        folder = request.GET.get("folder")
        file = request.GET.get("file")
        url = KmlPrefix + '/' + folder + '/' + file
        data = requests.get(url)
        responseData = HttpResponse(data)
        return responseData


def forecast(request):
    if request.method == 'GET':
        if request.GET.get('loc') == 'global':
            data = requests.get(WoForecastUrl, stream=True)
        else:
            data = requests.get(CaForecastUrl, stream=True)

        z = zipfile.ZipFile(io.BytesIO(data.content))
        responseData = HttpResponse(z.open('doc.kml'))
        return responseData


def gdacs(request):
    if request.method == 'GET':
        data = requests.get(GdacsUrl)
        responseData = HttpResponse(data)
        return responseData


def nowcast_plots(request):
    if request.method == 'GET':
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")
        payload = {
            'location': lat + ',' + lon,
            'name': request.GET.get("place"),
            'country': 'notset',
        }
        data = requests.get(NowcastUrl, params=payload)
        print(data.request.url)
        print(data.text)
        responseData = HttpResponse(data)
        return responseData


def dislocInput(request):
    if request.method == 'POST':
        print("test")
        file = request.FILES['file']
        inputFile = user_storage.save_input_file(request, file)
        print(inputFile.productUri + ' uri')
        id = 'Disloc_d9f189ed-d2c1-4e07-b709-de736f487e89'
        return JsonResponse(
            {
            "app_id": id,
            "Disloc Input File": inputFile.productUri,

            }
        )



def uavsarOverview(request):
    if request.method == 'GET':
        data = requests.get(wmsUrl)
        responseData = HttpResponse(data)
        return responseData

def seismicity(request):
    if request.method == 'GET':
        uri = request.GET.get('fullUri')
        data = requests.get(uri)
        responseData = HttpResponse(data)
        return responseData

def uavsarGeometry(request):
    if request.method == 'GET':
        if request.GET.get('type') == 'point':
            point = request.GET.get('queryStr')
            fullQuery = uavsarJsonUrl + 'Point:' + point
        elif request.GET.get('type') == 'polygon':
            poly = request.GET.get('queryStr')
            fullQuery = uavsarJsonUrl + 'Polygon:' + poly
        else:
            rect = request.GET.get('queryStr')
            fullQuery = uavsarJsonUrl + 'Rectangle:' + rect

        data = requests.get(fullQuery)
        responseData = HttpResponse(data)
        return responseData


def uavsarFlight(request):
    if request.method == 'GET':
        path = request.GET.get('queryStr')
        fullUri = geoServerUrl + path
        data = requests.get(fullUri)
        responseData = HttpResponse(data)
        return responseData

def uavsarTest(request):
    if request.method == 'GET':
        testURI = 'version=1.1.1&request=DescribeLayer&outputFormat=application/json&exceptions=application/json&layers= '

        uid = request.GET.get('uid')
        uid = str(uid)
        layername = 'InSAR:' + 'uid' + uid + '_unw'

        # test if it has coloring layer
        geoserver_response = requests.get(wmsColorUrl + testURI + layername)
        data = geoserver_response.json()
        checkdict = {'layer':layername}
        if "layerDescriptions" in data:
            checkdict['hasAlternateColoring'] = 1
            
        # test if it has highres layer
        geoserver_response = requests.get(wmsUrl + testURI + layername)
        data = geoserver_response.json()
        if "layerDescriptions" in data:
            checkdict['hasHighresOverlay'] = 1
        else:
            # get lowres kml
            baseURI = 'https://data.geo-gateway.org/kmz/'
            dataname = request.GET.get('dataname')
            postfix = 'uid' + uid + '/' + dataname + '.unw.kml'
            kmldata = requests.get(baseURI + postfix)
            toRep = '<href>https://data.geo-gateway.org/kmz/' + 'uid' + uid + '/'
            respData = kmldata.content.replace('<href>'.encode(), toRep.encode()).decode("utf-8")
            checkdict['lowreskml'] = respData
        return HttpResponse(json.dumps(checkdict))


def uavsarKML(request):
    if request.method == 'GET':

        #baseURI = 'http://gf2.ucs.indiana.edu/kmz/'
        baseURI = 'https://data.geo-gateway.org/kmz/'

        raw = request.GET.get('json')
        query = json.loads(raw)
        postfix = 'uid' + query['uid'] + '/' + query['dataname'] + '.unw.kml'
        fullURI = baseURI + postfix
        data = requests.get(fullURI)

        uid = query['uid']

        #toRep = '<href>http://gf2.ucs.indiana.edu/kmz/' + 'uid' + uid + '/'
        toRep = '<href>https://data.geo-gateway.org/kmz/' + 'uid' + uid + '/'

        respData = data.content.replace('<href>'.encode(), toRep.encode()).decode("utf-8")
        meta = query
        responseObj = {'kml': respData, 'info': meta, 'displayed': True, 'active': True, 'extended': False}

        response = JsonResponse(responseObj, safe=False)
        return response


def uavsarCSV(request):
    if request.method == 'GET':
        # http://149.165.157.193:8000/los/profile?image=uid475_unw&point=-115.8003008515625,33.56101488057798,-115.7003008515625,33.56101488057798&format=csv&resolution=undefined&method=native
        # raw = request.GET.get('entry')
        # entry = json.loads(raw)
        # info = entry['info']
        # uid = info['uid']
        uid = request.GET.get('uid')
        image_name = request.GET.get('dataname')
        # image_name = info['dataname']
        lat1 = request.GET.get('lat1')
        lon1 = request.GET.get('lon1')
        lat2 = request.GET.get('lat2')
        lon2 = request.GET.get('lon2')
        losLength = request.GET.get('losLength')
        azimuth = request.GET.get('azimuth')

        finalURI = losQueryUrl + uid + '_unw&point=' + lon1 + ',' + lat1 + ',' + lon2 + ',' + lat2 + \
                   '&format=csv&resolution=undefined&method=native'


        data = requests.get(finalURI)

        data = str(data.content.decode())

        data = data.replace('""', '')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + uid + '.csv"'

        writer = csv.writer(response)
        writer.writerow([image_name])
        writer.writerow(['start', lat1, lon1])
        writer.writerow(['end', lat2, lon2])
        writer.writerow(['azimuth', azimuth])
        writer.writerow(['length', losLength])
        writer.writerow("Lon, Lat, Distance (km), Displacement, Elevation Angle".split(','))
        data = data.splitlines()
        data = [line.split(',') for line in data]
        writer.writerows(data)

#         data = ContentFile(data)

        return response
#         fs = FileSystemStorage()
#         filename = fs.save(uid + '.csv', data)
#         uploaded_file_url = fs.url(filename)
#         return HttpResponse(uploaded_file_url, content_type='text/plain')


def losDownload(request):
    if request.method == 'GET':
        # http://149.165.157.193:8000/los/profile?image=uid475_unw&point=-115.8003008515625,33.56101488057798,-115.7003008515625,33.56101488057798&format=csv&resolution=undefined&method=native
        raw = request.GET.get('entry')
        entry = json.loads(raw)
        info = entry['info']
        uid = info['uid']
        image_name = info['dataname']
        lat1 = request.GET.get('lat1')
        lon1 = request.GET.get('lon1')
        lat2 = request.GET.get('lat2')
        lon2 = request.GET.get('lon2')
        losLength = request.GET.get('losLength')
        azimuth = request.GET.get('azimuth')

        finalURI = losQueryUrl + uid + '_unw&point=' + lon1 + ',' + lat1 + ',' + lon2 + ',' + lat2 + \
                   '&format=csv&resolution=undefined&method=native'

        data = requests.get(finalURI)

        data = str(data.content.decode())

        data = data.replace('""', '')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + uid + '.csv"'

        writer = csv.writer(response)
        writer.writerow([image_name])
        writer.writerow(['Start', lat1, lon1])
        writer.writerow(['End', lat2, lon2])
        writer.writerow(['Azimuth', azimuth])
        writer.writerow(['Length (km)', losLength])
        writer.writerow("Lon, Lat, Distance (km), Displacement (cm), Elevation Angle, DEM (m)".split(','))
        data = data.splitlines()
        data = [line.split(',') for line in data]
        writer.writerows(data)

        #data = ContentFile(data)
        #fs = FileSystemStorage()
        #filename = fs.save(uid + '.csv', data)
        #uploaded_file_url = fs.url(filename)
        #return HttpResponse(uploaded_file_url, content_type='text/plain')
        return response





def kmz_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        return HttpResponse(uploaded_file_url, content_type='text/plain')

def kml_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        return HttpResponse(uploaded_file_url, content_type='text/plain')

