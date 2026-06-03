from django.urls import path
from . import views

app_name = 'mascotas'

urlpatterns = [
    path('', views.MascotaListView.as_view(), name='lista_mascotas'),
    path('<int:pk>/', views.MascotaDetailView.as_view(), name='detalle_mascota'),
    path('nueva/', views.MascotaCreateView.as_view(), name='crear_mascota'),
    path('<int:pk>/editar/', views.MascotaUpdateView.as_view(), name='editar_mascota'),
    path('<int:pk>/eliminar/', views.MascotaDeleteView.as_view(), name='eliminar_mascota'),
]