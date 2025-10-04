from rest_framework import serializers
from core.entities.categoria import Categoria

class CategoriaSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(
        max_length=50,
        min_length=3,
        trim_whitespace=True
    )
    activa = serializers.BooleanField(default=True, read_only=True)
    fecha_creacion = serializers.DateTimeField(read_only=True)
    
    def validate_nombre(self, value):
        """Validación personalizada del nombre"""
        value = value.strip().title()
        
        # Validar longitud
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        if len(value) > 50:
            raise serializers.ValidationError("El nombre no puede exceder 50 caracteres")
        
        # Validar formato (solo letras y espacios)
        if not all(c.isalpha() or c.isspace() for c in value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios")
        
        return value
    
    def create(self, validated_data):
        """Crear entidad a partir de datos validados"""
        return Categoria(**validated_data)
    
    def update(self, instance, validated_data):
        """Actualizar entidad existente"""
        # Como nuestra entidad es inmutable, creamos una nueva
        return Categoria(
            id=instance.id,
            nombre=validated_data.get('nombre', instance.nombre),
            fecha_creacion=instance.fecha_creacion,
            activa=validated_data.get('activa', instance.activa)
        )