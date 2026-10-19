from django.contrib import admin
from django.urls import path
from feed.views import home, connect, download_vcard, sitemap
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('connect/', connect, name='connect'),
    path('connect/vcard.vcf', download_vcard, name='download_vcard'),
    path('sitemap.xml', sitemap, name='sitemap'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
