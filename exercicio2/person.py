import re
from dataclasses import dataclass, field
from typing import List

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s.]+\.[^@\s]+$")

ERRO_NOME_PARTES = "O nome deve ser composto por ao menos 2 partes."
ERRO_NOME_LETRAS = "O nome deve conter apenas letras."
ERRO_IDADE = "A idade deve estar no intervalo [1, 151]."
ERRO_SEM_EMAIL = "A pessoa deve ter ao menos um e-mail associado."
ERRO_EMAIL_FORMATO = "E-mail em formato inválido: {}"


@dataclass
class Email:
    name: str


@dataclass
class Person:
    name: str
    age: int
    emails: List[Email] = field(default_factory=list)


class PersonDAO:
    def isValidToInclude(self, person: Person) -> List[str]:
        erros: List[str] = []
        erros.extend(self._validar_nome(person.name))
        erros.extend(self._validar_idade(person.age))
        erros.extend(self._validar_emails(person.emails))
        return erros

    @staticmethod
    def _validar_nome(nome) -> List[str]:
        partes = nome.split() if isinstance(nome, str) else []
        erros = []
        if len(partes) < 2:
            erros.append(ERRO_NOME_PARTES)
        if not partes or not all(parte.isalpha() for parte in partes):
            erros.append(ERRO_NOME_LETRAS)
        return erros

    @staticmethod
    def _validar_idade(idade) -> List[str]:
        if isinstance(idade, bool) or not isinstance(idade, int) or not 1 <= idade <= 151:
            return [ERRO_IDADE]
        return []

    @staticmethod
    def _validar_emails(emails) -> List[str]:
        if not emails:
            return [ERRO_SEM_EMAIL]
        return [
            ERRO_EMAIL_FORMATO.format(email.name)
            for email in emails
            if not isinstance(email.name, str) or not EMAIL_REGEX.match(email.name)
        ]
