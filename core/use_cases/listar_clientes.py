from typing import List
from core.entities.cliente import Cliente
from core.repositories.cliente_repository import ClienteRepository

class ListarClientes:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self) -> List[Cliente]:
        return self.cliente_repository.list_all()
