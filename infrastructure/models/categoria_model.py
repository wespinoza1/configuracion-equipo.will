from django.db import models
from django.core.validators import RegexValidator

class CategoriaModel(models.Model):

    nombre = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúñÑ\s]+$',
                message='El nombre solo puede contener letras y espacios'
            )
        ]
    )
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def soft_delete(self):
        """Eliminación lógica"""
        self.activa = False
        self.save(update_fields=['activa'])

    def activate(self):
        """Reactivar categoría"""
        self.activa = True
        self.save(update_fields=['activa'])