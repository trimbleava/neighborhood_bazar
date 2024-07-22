from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import (permission_denied,
                                   page_not_found,
                                   server_error)
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView

# customize admin page
admin.site.site_header = 'Neighborhood Bazaar Admin Page'
admin.site.site_title = 'Neighborhood Bazaar'
admin.site.site_url = 'http://localhost:8000/admin'
admin.site.index_title = 'Neighborhood Bazaar Administration'
admin.empty_value_display = '**Empty**'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path('', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Show error pages during development
    urlpatterns += [
        re_path(r'^403/$', permission_denied),
        re_path(r'^404/$', page_not_found),
        re_path(r'^500/$', server_error)
    ]

