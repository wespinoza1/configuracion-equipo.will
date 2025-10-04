from rest_framework import serializers
from core.entities.detalleventa import DetalleVenta


class DetalleVentaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    notaventa_id = serializers.IntegerField()
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField()
    precio_venta = serializers.FloatField()

    def to_representation(self, instance: DetalleVenta):
        """Convierte la entidad a JSON"""
        return {
            "id": instance.id,
            "notaventa_id": instance.notaventa_id,
            "producto_id": instance.producto_id,
            "cantidad": instance.cantidad,
            "precio_venta": instance.precio_venta,
        }


