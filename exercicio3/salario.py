from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


class Cargo(Enum):
    DESENVOLVEDOR = "DESENVOLVEDOR"
    DBA = "DBA"
    TESTADOR = "TESTADOR"
    GERENTE = "GERENTE"


@dataclass(frozen=True)
class RegraDesconto:
    limite: Decimal
    desconto_acima_ou_igual: Decimal
    desconto_abaixo: Decimal

    def desconto_para(self, salario: Decimal) -> Decimal:
        return self.desconto_acima_ou_igual if salario >= self.limite else self.desconto_abaixo


REGRAS = {
    Cargo.DESENVOLVEDOR: RegraDesconto(Decimal("3000.00"), Decimal("0.20"), Decimal("0.10")),
    Cargo.DBA: RegraDesconto(Decimal("2000.00"), Decimal("0.25"), Decimal("0.15")),
    Cargo.TESTADOR: RegraDesconto(Decimal("2000.00"), Decimal("0.25"), Decimal("0.15")),
    Cargo.GERENTE: RegraDesconto(Decimal("5000.00"), Decimal("0.30"), Decimal("0.20")),
}


@dataclass
class Funcionario:
    nome: str
    email: str
    salario_base: Decimal
    cargo: Cargo

    def __post_init__(self):
        self.salario_base = Decimal(str(self.salario_base))
        if self.salario_base < 0:
            raise ValueError("O salário-base não pode ser negativo.")
        if not isinstance(self.cargo, Cargo):
            raise ValueError(f"Cargo inválido: {self.cargo}")


class CalculadoraSalario:
    def calcular_salario_liquido(self, funcionario: Funcionario) -> Decimal:
        regra = REGRAS[funcionario.cargo]
        desconto = regra.desconto_para(funcionario.salario_base)
        liquido = funcionario.salario_base * (Decimal("1") - desconto)
        return liquido.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
