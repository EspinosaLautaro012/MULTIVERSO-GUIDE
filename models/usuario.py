class Usuario:
    """Representa al usuario que consulta el sistema."""

    PERFILES_VALIDOS = ("fan", "casual")

    def __init__(self, nombre, perfil="casual"):
        self._nombre = nombre
        self._perfil = perfil if perfil in self.PERFILES_VALIDOS else "casual"
        self._obras_vistas = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def perfil(self):
        return self._perfil

    @perfil.setter
    def perfil(self, valor):
        if valor in self.PERFILES_VALIDOS:
            self._perfil = valor

    @property
    def obras_vistas(self):
        return list(self._obras_vistas)

    def marcar_vista(self, titulo_obra):
        if titulo_obra not in self._obras_vistas:
            self._obras_vistas.append(titulo_obra)

    def __repr__(self):
        return f"Usuario({self._nombre}, perfil={self._perfil})"
