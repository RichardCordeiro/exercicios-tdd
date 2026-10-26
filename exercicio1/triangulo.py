from enum import Enum


class TipoTriangulo(Enum):
    EQUILATERO = "equilátero"
    ISOSCELES = "isósceles"
    ESCALENO = "escaleno"


class TrianguloInvalidoError(ValueError):
    """Lançada quando os três lados informados não formam um triângulo."""


class Triangulo:
    def __init__(self, a: int, b: int, c: int):
        self.lados = (a, b, c)
        self._validar()

    def _validar(self) -> None:
        a, b, c = self.lados
        if any(not isinstance(lado, int) or isinstance(lado, bool) for lado in self.lados):
            raise TrianguloInvalidoError("Os lados devem ser números inteiros.")
        if any(lado <= 0 for lado in self.lados):
            raise TrianguloInvalidoError("Os lados devem ser maiores que zero.")
        if a + b <= c or a + c <= b or b + c <= a:
            raise TrianguloInvalidoError(
                "A soma de dois lados deve ser maior que o terceiro lado."
            )

    def classificar(self) -> TipoTriangulo:
        distintos = len(set(self.lados))
        if distintos == 1:
            return TipoTriangulo.EQUILATERO
        if distintos == 2:
            return TipoTriangulo.ISOSCELES
        return TipoTriangulo.ESCALENO
