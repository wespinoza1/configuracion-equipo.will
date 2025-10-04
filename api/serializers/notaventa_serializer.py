from rest_framework import serializers
from infrastructure.models.notaventa_model import NotaVentaModel
from infrastructure.models.cliente_model import ClienteModel


class NotaVentaSerializer(serializers.ModelSerializer):
    """
    Serializer para representar y validar Notas de Venta.
    Maneja el ID del cliente como entrada y salida.
    """

    cliente_id = serializers.IntegerField()  # lectura + escritura

    class Meta:
        model = NotaVentaModel
        fields = ["id", "cliente_id", "monto", "fecha", "activo"]
        read_only_fields = ["id", "fecha", "activo"]

    def create(self, validated_data):
        """
        Crea una nueva Nota de Venta con el cliente referenciado por su ID.
        """
        cliente_id = validated_data.pop("cliente_id")
        cliente = ClienteModel.objects.get(pk=cliente_id)
        return NotaVentaModel.objects.create(cliente=cliente, **validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza una Nota de Venta existente.
        """
        cliente_id = validated_data.pop("cliente_id", None)
        if cliente_id:
            instance.cliente = ClienteModel.objects.get(pk=cliente_id)

        instance.monto = validated_data.get("monto", instance.monto)
        instance.save()
        return instance
