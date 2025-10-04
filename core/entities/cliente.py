from typing import Optional
import re

"""
Entidad de dominio Cliente
El ID es independiente de cómo se genera, 
pero en este caso lo tratamos como int (autoincremental en la BD).
"""

class Cliente:
    def __init__(
        self,
        nombre: str,
        apellido_paterno: str,
        apellido_materno: str,
        direccion: str,
        telefono: str,
        id: Optional[int] = None,  # 👈 int incremental
    ):
        # Normalización de datos
        self._id = id
        self._nombre = nombre.strip().title()
        self._apellido_paterno = apellido_paterno.strip().title()
        self._apellido_materno = apellido_materno.strip().title()
        self._direccion = direccion.strip()
        self._telefono = telefono.strip().replace(" ", "")

        # Validaciones invariantes
        self._validar_nombre()
        self._validar_apellidos()
        self._validar_telefono()

    def __str__(self) -> str:
        return f'{self.nombre_completo} ({self.id})'

    # -------- Propiedades (inmutabilidad parcial) --------
    @property
    def id(self) -> Optional[int]: return self._id

    @property
    def nombre(self) -> str: return self._nombre

    @property
    def apellido_paterno(self) -> str: return self._apellido_paterno

    @property
    def apellido_materno(self) -> str:return self._apellido_materno

    @property
    def direccion(self) -> str: return self._direccion

    @property
    def telefono(self) -> str: return self._telefono

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido_paterno} {self._apellido_materno}"

    # -------- Validaciones --------
    def _validar_nombre(self):
        if len(self._nombre) < 3:
            raise ValueError("El nombre del cliente debe tener al menos 3 caracteres")

    def _validar_apellidos(self):
        if not self._apellido_paterno or not self._apellido_materno:
            raise ValueError("Ambos apellidos son obligatorios")

    def _validar_telefono(self):
        # Acepta números nacionales e internacionales con +, mínimo 7 dígitos
        if not re.match(r"^\+?\d{7,15}$", self._telefono):
            raise ValueError("El teléfono no es válido")

    # -------- Comportamientos de negocio --------
    def cambiar_direccion(self, nueva_direccion: str):
        if not nueva_direccion or len(nueva_direccion.strip()) < 5:
            raise ValueError("La dirección no es válida")
        self._direccion = nueva_direccion.strip()

    def actualizar_telefono(self, nuevo_telefono: str):
        nuevo_telefono = nuevo_telefono.strip().replace(" ", "")
        if not re.match(r"^\+?\d{7,15}$", nuevo_telefono):
            raise ValueError("El teléfono no es válido")
        self._telefono = nuevo_telefono


    def cambiar_nombre(self, nuevo_nombre: str):
        self._nombre = nuevo_nombre.strip().title()
        self._validar_nombre()

    def cambiar_apellido_paterno(self, nuevo_apellido: str):
        self._apellido_paterno = nuevo_apellido.strip().title()
        self._validar_apellidos()

    def cambiar_apellido_materno(self, nuevo_apellido: str):
        self._apellido_materno = nuevo_apellido.strip().title()
        self._validar_apellidos()


    # -------- Comparaciones --------
    def __eq__(self, other):
        if isinstance(other, Cliente):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
