from django.urls import path
from . import views
from .views import delete_photo

app_name = 'bicicletas'

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos_view, name='productos'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('contacto/', views.contacto, name='contacto'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('publicacion/nueva/', views.gestionar_publicacion, name='nueva_publicacion'),
    path('publicacion/editar/<int:publicacion_id>/', views.gestionar_publicacion, name='editar_publicacion'),
    path('publicaciones/', views.lista_publicaciones, name='lista_publicaciones'),
    path('bicycle/publicar/', views.publish_bicycle, name='publish_bicycle'),
    path('mis-publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
    path('eliminar-publicacion/<int:publicacion_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('photo/<int:image_id>/delete/', delete_photo, name='delete_photo'),
]



