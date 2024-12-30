from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver    
from django.core.mail import send_mail


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    ESTADOS = [
        ('NUEVO', 'Nuevo'),
        ('USADO', 'Usado'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.get_estado_display()} - {self.precio}"
    
    
class Bicycle(models.Model):
    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
    ]
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    color = models.CharField(max_length=50)
    rodado = models.PositiveIntegerField()
    estado = models.CharField(max_length=5, choices=ESTADO_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class BicycleImage(models.Model):
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='bicycle_images/')

    def __str__(self):
        return f"Image for {self.bicycle.titulo}"


class Mensaje(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    respuesta = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"
    

@receiver(post_save, sender=Mensaje)
def enviar_respuesta_email(sender, instance, created, **kwargs):
    if instance.respuesta and not created:  
        send_mail(
            subject=f"Respuesta a tu consulta: {instance.asunto}",
            message=(
                f"Hola {instance.nombre},\n\n"
                f"Gracias por contactarnos. Aquí está nuestra respuesta a tu consulta:\n\n"
                f"{instance.respuesta}\n\n"
                "Saludos cordiales,\nEl equipo de HOKO BIKES"
            ),
            from_email='tu-correo@dominio.com',
            recipient_list=[instance.email],
        )



    publicacion = models.ForeignKey(Bicycle, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='bicicletas/fotos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

