from rest_framework import serializers


class ClienteSerializer(serializers.Serializer):
    """
    Serializer para validar la entrada/salida de datos de Cliente en la API.
    No contiene lógica de negocio, solo validación de request/response.
    este serializer es un codigo manual y valido
    """

    id = serializers.UUIDField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    apellido_paterno = serializers.CharField(max_length=100)
    apellido_materno = serializers.CharField(max_length=100)
    direccion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=20)

    def validate_telefono(self, value):
        """Validación extra de formato de teléfono"""
        if not value.isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo números")
        if len(value) < 7 or len(value) > 9:
            raise serializers.ValidationError("El teléfono debe tener entre 7 y 9 dígitos")
        return value


'''
este es un ejemplo de serializers de configuracion automatica con el modelo

from rest_framework import serializers
from infrastructure.models.cliente_model import ClienteModel

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteModel
        fields = "__all__"
'''