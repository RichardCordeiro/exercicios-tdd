from decimal import Decimal

import pytest

from exercicio3.salario import CalculadoraSalario, Cargo, Funcionario


@pytest.fixture
def calculadora():
    return CalculadoraSalario()


def funcionario(salario, cargo):
    return Funcionario("Fulano de Tal", "fulano@empresa.com", salario, cargo)


# Para cada cargo: abaixo do limite, exatamente no limite (fronteira) e acima do limite.
@pytest.mark.parametrize(
    "cargo, salario, esperado",
    [
        # DESENVOLVEDOR: >= 3.000 -> 20%, senão 10%
        (Cargo.DESENVOLVEDOR, "2999.99", "2699.99"),
        (Cargo.DESENVOLVEDOR, "3000.00", "2400.00"),
        (Cargo.DESENVOLVEDOR, "5500.00", "4400.00"),
        (Cargo.DESENVOLVEDOR, "1000.00", "900.00"),
        # DBA: >= 2.000 -> 25%, senão 15%
        (Cargo.DBA, "1999.99", "1699.99"),
        (Cargo.DBA, "2000.00", "1500.00"),
        (Cargo.DBA, "3000.00", "2250.00"),
        (Cargo.DBA, "500.00", "425.00"),
        # TESTADOR: >= 2.000 -> 25%, senão 15%
        (Cargo.TESTADOR, "1999.99", "1699.99"),
        (Cargo.TESTADOR, "2000.00", "1500.00"),
        (Cargo.TESTADOR, "2500.00", "1875.00"),
        (Cargo.TESTADOR, "550.00", "467.50"),
        # GERENTE: >= 5.000 -> 30%, senão 20%
        (Cargo.GERENTE, "4999.99", "3999.99"),
        (Cargo.GERENTE, "5000.00", "3500.00"),
        (Cargo.GERENTE, "7000.00", "4900.00"),
        (Cargo.GERENTE, "2500.00", "2000.00"),
    ],
)
def test_salario_liquido_por_cargo(calculadora, cargo, salario, esperado):
    resultado = calculadora.calcular_salario_liquido(funcionario(Decimal(salario), cargo))
    assert resultado == Decimal(esperado)


def test_salario_zero(calculadora):
    assert calculadora.calcular_salario_liquido(funcionario(0, Cargo.DBA)) == Decimal("0.00")


def test_aceita_salario_float_ou_int(calculadora):
    assert calculadora.calcular_salario_liquido(funcionario(3000, Cargo.DESENVOLVEDOR)) == Decimal("2400.00")
    assert calculadora.calcular_salario_liquido(funcionario(2999.99, Cargo.DESENVOLVEDOR)) == Decimal("2699.99")


def test_arredonda_para_centavos(calculadora):
    # 1234.57 * 0.90 = 1111.113 -> 1111.11
    assert calculadora.calcular_salario_liquido(funcionario("1234.57", Cargo.DESENVOLVEDOR)) == Decimal("1111.11")


def test_funcionario_guarda_dados():
    f = Funcionario("Ana Lima", "ana@empresa.com", Decimal("4000"), Cargo.GERENTE)
    assert (f.nome, f.email, f.salario_base, f.cargo) == (
        "Ana Lima",
        "ana@empresa.com",
        Decimal("4000"),
        Cargo.GERENTE,
    )


def test_salario_negativo_e_rejeitado():
    with pytest.raises(ValueError):
        funcionario(Decimal("-1"), Cargo.DBA)


def test_cargo_invalido_e_rejeitado():
    with pytest.raises(ValueError):
        funcionario(Decimal("1000"), "ESTAGIARIO")
