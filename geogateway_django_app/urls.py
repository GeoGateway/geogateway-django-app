from django.urls import re_path
from django.views.generic import TemplateView
from rest_framework import routers
from . import GeoGatewayData
from . import views

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

app_name = "geogateway_django_app"



urlpatterns = [
    re_path(r'^$',
        views.frontend,
        name="home",
        ),
    re_path(r"^gps_service/", GeoGatewayData.gps_service),
    re_path(r"^get_kml/", GeoGatewayData.get_gnss_kml),
    re_path(r"^wo_forecast/", GeoGatewayData.forecast),
    re_path(r"^ca_forecast/", GeoGatewayData.forecast),
    re_path(r"^gdacs/", GeoGatewayData.gdacs),
    #re_path(r"^nowcast/", GeoGatewayData.nowcast_plots),
    re_path(r"^disloc/", GeoGatewayData.dislocInput),
    re_path(r'^kml_upload/$', GeoGatewayData.kml_upload),
    re_path(r"^UAVSAR_overview/", GeoGatewayData.uavsarOverview),
    re_path(r"^UAVSAR_geom/", GeoGatewayData.uavsarGeometry),
    re_path(r"^UAVSAR_KML/", GeoGatewayData.uavsarKML),
    re_path(r"^UAVSAR_test/", GeoGatewayData.uavsarTest),
    re_path(r"^UAVSAR_csv/", GeoGatewayData.uavsarCSV),
    re_path(r"^UAVSAR_flight/", GeoGatewayData.uavsarFlight),
    re_path(r'^kmz_upload/$', GeoGatewayData.kmz_upload),
    re_path(r'^seismicity/$', GeoGatewayData.seismicity),
    re_path(r'^los_download/$', GeoGatewayData.losDownload)



]
