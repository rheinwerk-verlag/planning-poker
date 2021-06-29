from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

from . import views

app_name = 'planning_poker'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.PokerSessionView.as_view(), name='poker_session'),
    path('jsi18n/',
         JavaScriptCatalog.as_view(packages=['planning_poker']),
         name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
]
