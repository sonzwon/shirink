from shortener.forms import UrlCreateForm
from django.contrib import admin
from django.urls import path
from shortener.urls.views import url_list, url_create, url_change, statistic_view, qr_create, qr_list, qr_show

from rest_framework import routers
from shortener.urls.apis import *
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"urls", UrlListView)
router.register(r"qrs", QrListView)

urlpatterns = [
    path("", url_list, name="url_list"),
    path("create", url_create, name="url_create"),
    path("qrlist/", qr_list, name="qr_list"),
    path("qrcreate/", qr_create, name="qr_create"),
    path("qrshow/", qr_show, name="qr_show"),
    path("<str:action>/<int:url_id>", url_change, name="url_change"),
    path("<int:url_id>/statistic", statistic_view, name="statistic_view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
