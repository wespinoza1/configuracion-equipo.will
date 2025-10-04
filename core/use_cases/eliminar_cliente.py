from core.repositories.cliente_repository import ClienteRepository

class EliminarCliente:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_id: int) -> None:
        self.cliente_repository.delete(cliente_id)
