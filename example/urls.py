from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.urls import include, path

urlpatterns = [
    path('jsi18n/',
         JavaScriptCatalog.as_view(packages=['planning_poker']),
         name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('poker/', include('planning_poker.urls')),
]
