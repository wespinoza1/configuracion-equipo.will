from core.entities.cliente import Cliente
from core.repositories.cliente_repository import ClienteRepository


"""Caso de uso: Registrar un nuevo cliente en el sistema."""
class RegistrarCliente:

    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, data: dict) -> Cliente:
        """
        Recibe un diccionario con los datos validados del cliente.
        Crea la entidad Cliente y la persiste en el repositorio.
        """

        # Crear la entidad de dominio con los datos
        cliente = Cliente(
            nombre=data["nombre"],
            apellido_paterno=data["apellido_paterno"],
            apellido_materno=data["apellido_materno"],
            direccion=data["direccion"],
            telefono=data["telefono"]
        )

        # Persistir usando el repositorio
        return self.cliente_repository.save(cliente)

