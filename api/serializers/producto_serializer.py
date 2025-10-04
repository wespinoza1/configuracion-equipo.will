from rest_framework import serializers
from core.entities.producto import Producto
from core.entities.categoria import Categoria


class ProductoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    descripcion = serializers.CharField(max_length=100, min_length=3, trim_whitespace=True)
    precio = serializers.FloatField(min_value=0.01)
    stock = serializers.IntegerField(min_value=0)

    # entrada: categoria_id requerido; salida lo construimos en to_representation
    categoria_id = serializers.IntegerField(write_only=True, required=True)

    # permitir que 'activo' se pueda enviar en updates (opcional)
    activo = serializers.BooleanField(required=False)

    def to_representation(self, instance: Producto):
        """Construir salida plana (incluye categoria_id desde instance.categoria.id)."""
        return {
            "id": instance.id,
            "descripcion": instance.descripcion,
            "precio": instance.precio,
            "stock": instance.stock,
            "categoria_id": instance.categoria.id if getattr(instance, "categoria", None) else None,
            "activo": instance.activo,
        }

    def validate_descripcion(self, value):
        value = value.strip().title()
        if len(value) < 3:
            raise serializers.ValidationError("La descripción debe tener al menos 3 caracteres")
        if len(value) > 100:
            raise serializers.ValidationError("La descripción no puede exceder 100 caracteres")
        return value

    def create(self, validated_data):
        categoria_id = validated_data["categoria_id"]
        categoria = Categoria(id=categoria_id, nombre="")
        activo = validated_data.get("activo", True)
        return Producto(
            descripcion=validated_data["descripcion"],
            precio=validated_data["precio"],
            stock=validated_data["stock"],
            categoria=categoria,
            activo=activo
        )

    def update(self, instance: Producto, validated_data):
        categoria_id = validated_data.get("categoria_id", instance.categoria.id)
        categoria = Categoria(id=categoria_id, nombre=getattr(instance.categoria, "nombre", ""))
        return Producto(
            id=instance.id,
            descripcion=validated_data.get("descripcion", instance.descripcion),
            precio=validated_data.get("precio", instance.precio),
            stock=validated_data.get("stock", instance.stock),
            categoria=categoria,
            activo=validated_data.get("activo", instance.activo)
        )
