from uuid import UUID
from core.entities.cliente import Cliente
from core.repositories.cliente_repository import ClienteRepository


class ActualizarCliente:
    """
    Caso de uso: actualizar los datos de un cliente existente.
    Recibe el cliente_id y un diccionario con los campos a actualizar.
    """

    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_id: UUID, data: dict) -> Cliente:
        # Obtener cliente desde repositorio
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        # Actualizar campos de la entidad según el diccionario recibido
        if "direccion" in data:
            cliente.cambiar_direccion(data["direccion"])
        if "telefono" in data:
            cliente.actualizar_telefono(data["telefono"])
        if "nombre" in data:
            cliente.cambiar_nombre(data["nombre"])
        if "apellido_paterno" in data:
            cliente.cambiar_apellido_paterno(data["apellido_paterno"])
        if "apellido_materno" in data:
            cliente.cambiar_apellido_materno(data["apellido_materno"])

        # Persistir cambios usando el repositorio
        return self.cliente_repository.save(cliente)
