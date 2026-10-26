import pytest

from exercicio2.person import (
    ERRO_EMAIL_FORMATO,
    ERRO_IDADE,
    ERRO_NOME_LETRAS,
    ERRO_NOME_PARTES,
    ERRO_SEM_EMAIL,
    Email,
    Person,
    PersonDAO,
)


@pytest.fixture
def dao():
    return PersonDAO()


def pessoa(name="Maria Silva", age=30, emails=None):
    if emails is None:
        emails = [Email("maria@email.com")]
    return Person(name=name, age=age, emails=emails)


def test_pessoa_valida_nao_retorna_erros(dao):
    assert dao.isValidToInclude(pessoa()) == []


# --- Nome ---
@pytest.mark.parametrize("nome", ["Maria Silva", "José da Conceição", "Ana  Maria  Souza"])
def test_nome_valido(dao, nome):
    assert dao.isValidToInclude(pessoa(name=nome)) == []


def test_nome_com_uma_parte(dao):
    assert dao.isValidToInclude(pessoa(name="Maria")) == [ERRO_NOME_PARTES]


@pytest.mark.parametrize("nome", ["Maria S1lva", "Maria Silva!", "Maria Silva-Souza"])
def test_nome_com_caracteres_que_nao_sao_letras(dao, nome):
    assert dao.isValidToInclude(pessoa(name=nome)) == [ERRO_NOME_LETRAS]


@pytest.mark.parametrize("nome", ["", "   ", None])
def test_nome_vazio_ou_ausente(dao, nome):
    assert dao.isValidToInclude(pessoa(name=nome)) == [ERRO_NOME_PARTES, ERRO_NOME_LETRAS]


def test_nome_com_uma_parte_e_numeros(dao):
    assert dao.isValidToInclude(pessoa(name="Maria123")) == [ERRO_NOME_PARTES, ERRO_NOME_LETRAS]


@pytest.mark.parametrize("idade", [1, 2, 100, 150, 151])
def test_idade_dentro_do_intervalo(dao, idade):
    assert dao.isValidToInclude(pessoa(age=idade)) == []


@pytest.mark.parametrize("idade", [0, -1, 152, 1000])
def test_idade_fora_do_intervalo(dao, idade):
    assert dao.isValidToInclude(pessoa(age=idade)) == [ERRO_IDADE]


@pytest.mark.parametrize("idade", [None, "30", 30.5, True])
def test_idade_nao_inteira(dao, idade):
    assert dao.isValidToInclude(pessoa(age=idade)) == [ERRO_IDADE]


@pytest.mark.parametrize("emails", [[], None])
def test_sem_email(dao, emails):
    p = Person(name="Maria Silva", age=30, emails=emails)
    assert dao.isValidToInclude(p) == [ERRO_SEM_EMAIL]


@pytest.mark.parametrize("endereco", ["a@b.c", "maria.silva@fatec.sp.gov.br"])
def test_email_valido(dao, endereco):
    assert dao.isValidToInclude(pessoa(emails=[Email(endereco)])) == []


@pytest.mark.parametrize(
    "endereco",
    [
        "",
        "maria",
        "maria@email",
        "@email.com",
        "maria@.com",
        "maria@email.",
        "maria@@email.com",
        "maria silva@email.com",
        "maria.email.com",
    ],
)
def test_email_invalido(dao, endereco):
    assert dao.isValidToInclude(pessoa(emails=[Email(endereco)])) == [
        ERRO_EMAIL_FORMATO.format(endereco)
    ]


def test_email_com_valor_nao_texto(dao):
    assert dao.isValidToInclude(pessoa(emails=[Email(None)])) == [ERRO_EMAIL_FORMATO.format(None)]


def test_varios_emails_retorna_erro_apenas_dos_invalidos(dao):
    emails = [Email("ok@email.com"), Email("ruim"), Email("outro@x.y"), Email("x@y")]
    assert dao.isValidToInclude(pessoa(emails=emails)) == [
        ERRO_EMAIL_FORMATO.format("ruim"),
        ERRO_EMAIL_FORMATO.format("x@y"),
    ]


# --- Combinação ---
def test_todos_os_erros_ao_mesmo_tempo(dao):
    p = Person(name="M4ria", age=0, emails=[])
    assert dao.isValidToInclude(p) == [
        ERRO_NOME_PARTES,
        ERRO_NOME_LETRAS,
        ERRO_IDADE,
        ERRO_SEM_EMAIL,
    ]
