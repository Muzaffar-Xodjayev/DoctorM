from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler404
import myApp


urlpatterns = [
    path('11921179010125MMR/', admin.site.urls),
]+i18n_patterns(
    path('', include('myApp.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False
)+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

admin.site.site_header = 'Doctor M'
handler404 = myApp.views.error_404
