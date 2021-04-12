from django.urls import path

from . import views

app_name = 'planning_poker'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.PokerSessionView.as_view(), name='poker_session'),
]
