from django.db import models

"""
Modelo Django ORM para persistencia de Cliente.
No contiene lógica de negocio, solo mapeo a la base de datos.
"""

class ClienteModel(models.Model):
    id = models.AutoField(primary_key=True)  # 👈 autoincremental
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField('Paterno', max_length=60)
    apellido_materno = models.CharField('Materno', max_length=60)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, null=False, blank=False, unique=True)  # 👈 ampliado

    class Meta:
        db_table = "clientes"  # Nombre explícito de la tabla
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

