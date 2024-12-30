from django.contrib import admin
from .models import Bicycle, BicycleImage, Mensaje


@admin.register(Bicycle)
class BicycleAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'estado', 'precio', 'rodado')
    list_filter = ('estado', 'rodado')
    search_fields = ('titulo', 'descripcion', 'color')


@admin.register(BicycleImage)
class BicycleImageAdmin(admin.ModelAdmin):
    list_display = ('bicycle', 'image')
    search_fields = ('bicycle__titulo',)


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha_envio', 'respuesta')
    search_fields = ('nombre', 'email', 'asunto')
    list_editable = ('respuesta',)  