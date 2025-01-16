from django.urls import path
from .views import index, close, seedUserus

urlpatterns = [
    path('', index, name='index'),
    path('close/', close, name="close"),
    # path('createAsesores/', seedUserus, name="created")
]
