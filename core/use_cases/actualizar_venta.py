from typing import Optional, Union
from datetime import datetime
from core.repositories.notaventa_repository import NotaVentaRepository
from core.entities.notaventa import NotaVenta


class ActualizarVenta:
    """Caso de uso para actualizar una nota de venta existente."""

    def __init__(self, repo: NotaVentaRepository):
        self.repo = repo

    def ejecutar(
        self,
        id: Union[int, str],
        cliente_id: Optional[int] = None,
        monto: Optional[float] = None,
        fecha: Optional[Union[str, datetime]] = None,
    ) -> NotaVenta:
        """
        Actualiza una nota de venta existente.
        """
        # Buscar la venta existente
        nota_existente = self.repo.get_by_id(id)
        if not nota_existente:
            raise ValueError(f"No se encontró la nota de venta con id={id}")

        # Determinar cliente actualizado (por cliente_id)
        cliente_actualizado = cliente_id if cliente_id is not None else nota_existente.cliente_id

        # Determinar monto actualizado
        monto_actualizado = monto if monto is not None else nota_existente.monto
        if monto_actualizado < 0:
            raise ValueError("El monto de la nota de venta no puede ser negativo")

        # Determinar fecha actualizada
        if fecha:
            if isinstance(fecha, str):
                try:
                    fecha_actualizada = datetime.fromisoformat(fecha)
                except ValueError:
                    raise ValueError("Formato de fecha inválido, debe ser ISO 8601 (YYYY-MM-DDTHH:MM:SS)")
            elif isinstance(fecha, datetime):
                fecha_actualizada = fecha
            else:
                raise ValueError("La fecha debe ser str (ISO8601) o datetime")
        else:
            fecha_actualizada = nota_existente.fecha

        # Crear nueva instancia de NotaVenta (inmutable)
        nota_actualizada = NotaVenta(
            id=nota_existente.id,
            cliente_id=cliente_actualizado,
            monto=monto_actualizado,
            fecha=fecha_actualizada,
            activo=nota_existente.activo,
        )

        # Guardar cambios en el repositorio
        return self.repo.save(nota_actualizada)
