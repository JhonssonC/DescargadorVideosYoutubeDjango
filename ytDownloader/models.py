from django.db import models

# Create your models here.
class Video(models.Model):
    link = models.CharField('Enlace', max_length=120)
    resoluciones = models.CharField('Resoluciones', choices=(), blank=True, null = True, max_length=10)
    nombre = models.CharField('Nombre', blank=True, null = True, max_length=120)
    extension = models.CharField('Extension',  blank=True, null = True, max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.link + " - " + self.nombre