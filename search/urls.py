from django.urls import path
from .views import ReSearchView


urlpatterns = [
    path('search/', ReSearchView.as_view(), name='research')
]
