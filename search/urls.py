from django.conf.urls import url
from .views import reSearchView


urlpatterns = [
    url('search', reSearchView, name='research')
]
