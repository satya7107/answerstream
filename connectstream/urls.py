from django.urls import path, include

from .import views as aview

urlpatterns = [
    path('', aview.index, name='index'),
]