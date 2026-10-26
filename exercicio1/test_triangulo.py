import pytest

from exercicio1.triangulo import Triangulo, TipoTriangulo, TrianguloInvalidoError



def test_escaleno_valido():
    assert Triangulo(3, 4, 5).classificar() == TipoTriangulo.ESCALENO


def test_isosceles_valido():
    assert Triangulo(5, 5, 3).classificar() == TipoTriangulo.ISOSCELES


def test_equilatero_valido():
    assert Triangulo(4, 4, 4).classificar() == TipoTriangulo.EQUILATERO


@pytest.mark.parametrize("a, b, c", [(5, 5, 3), (5, 3, 5), (3, 5, 5)])
def test_isosceles_permutacoes(a, b, c):
    assert Triangulo(a, b, c).classificar() == TipoTriangulo.ISOSCELES


def test_um_valor_zero():
    with pytest.raises(TrianguloInvalidoError):
        Triangulo(0, 4, 5)


def test_um_valor_negativo():
    with pytest.raises(TrianguloInvalidoError):
        Triangulo(-3, 4, 5)


def test_soma_de_dois_lados_igual_ao_terceiro():
    with pytest.raises(TrianguloInvalidoError):
        Triangulo(1, 2, 3)


@pytest.mark.parametrize(
    "a, b, c",
    [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)],
)
def test_soma_igual_permutacoes(a, b, c):
    with pytest.raises(TrianguloInvalidoError):
        Triangulo(a, b, c)


def test_soma_de_dois_lados_menor_que_o_terceiro():
    with pytest.raises(TrianguloInvalidoError):
        Triangulo(1, 2, 5)


@pytest.mark.parametrize(
    "a, b, c",
    [(1, 2, 5), (1, 5, 2), (2, 1, 5), (2, 5, 1), (5, 1, 2), (5, 2, 1)],
)
def test_soma_menor_permutacoes(a, b, c):
    with pytest.raises(TrianguloInvalidoError):
        Triangulo(a, b, c)


def test_tres_valores_zero():
    with pytest.raises(TrianguloInvalidoError):
        Triangulo(0, 0, 0)


@pytest.mark.parametrize("a, b, c", [(3.5, 4, 5), ("3", 4, 5), (True, 4, 5)])
def test_lados_nao_inteiros(a, b, c):
    with pytest.raises(TrianguloInvalidoError):
        Triangulo(a, b, c)
