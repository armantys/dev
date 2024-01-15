# urls.py

from django.urls import path
from .views import lieuxListView, comparaisonListView, capteursListView, donneesMeteoListView

urlpatterns = [
    path('table1/', lieuxListView.as_view(), name='table1-list'),
    path('table2/', comparaisonListView.as_view(), name='table2-list'),
    path('table3/', capteursListView.as_view(), name='table3-list'),
    path('table4/', donneesMeteoListView.as_view(), name='table4-list'),
    # Ajoutez d'autres URLs selon vos besoins
]