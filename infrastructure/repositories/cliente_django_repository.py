from typing import List, Optional
from infrastructure.models.cliente_model import ClienteModel
from core.entities.cliente import Cliente
from core.repositories.cliente_repository import ClienteRepository


class ClienteDjangoRepository(ClienteRepository):

    def save(self, cliente: Cliente) -> Cliente:
        """Guarda o actualiza un Cliente en la base de datos."""
        if cliente.id:
            # Actualiza si existe
            ClienteModel.objects.filter(id=cliente.id).update(
                nombre=cliente.nombre,
                apellido_paterno=cliente.apellido_paterno,
                apellido_materno=cliente.apellido_materno,
                direccion=cliente.direccion,
                telefono=cliente.telefono,
            )
            obj = ClienteModel.objects.get(id=cliente.id)
        else:
            # Crea nuevo
            obj = ClienteModel.objects.create(
                nombre=cliente.nombre,
                apellido_paterno=cliente.apellido_paterno,
                apellido_materno=cliente.apellido_materno,
                direccion=cliente.direccion,
                telefono=cliente.telefono,
            )
        return self._map_to_entity(obj)

    def get_by_id(self, id: int) -> Optional[Cliente]:
        try:
            obj = ClienteModel.objects.get(id=id)
            return self._map_to_entity(obj)
        except ClienteModel.DoesNotExist:
            return None

    def list_all(self) -> List[Cliente]:
        clientes = ClienteModel.objects.all()
        return [self._map_to_entity(obj) for obj in clientes]

    def delete(self, id: int) -> None:
        ClienteModel.objects.filter(id=id).delete()

    # ----------- Mapper interno ----------- 
    def _map_to_entity(self, obj: ClienteModel) -> Cliente:
        return Cliente(
            id=obj.id,
            nombre=obj.nombre,
            apellido_paterno=obj.apellido_paterno,
            apellido_materno=obj.apellido_materno,
            direccion=obj.direccion,
            telefono=obj.telefono,
        )

