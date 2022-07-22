from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class articulo(models.Model):
    titulo = models.CharField("Articulo",max_length=200)
    subTitulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.CharField(max_length=200)
    imagen = models.ImageField(blank=True, null=True,upload_to='imagenes/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'


class Avatar(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)



class Mensaje(models.Model):
    usuario_receptor = models.ForeignKey(User, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autor')
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor}"


class Link(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    link1 = models.URLField(blank=True, null=True)
    link2 = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.link1

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

