from identita_studio.sicurezza import (
    cifra_password,
    impronta_token,
    token_opaco,
    verifica_password,
)


def test_password_giusta_verifica():
    impronta = cifra_password("una frase lunga che ricordo")
    assert verifica_password("una frase lunga che ricordo", impronta)


def test_password_sbagliata_non_verifica():
    impronta = cifra_password("una frase lunga che ricordo")
    assert not verifica_password("un'altra frase", impronta)


def test_impronta_malformata_non_esplode():
    assert not verifica_password("qualunque cosa", "non e' un hash argon2")


def test_token_opaco_non_si_ripete():
    assert token_opaco() != token_opaco()


def test_impronta_token_deterministica():
    token = token_opaco()
    assert impronta_token(token) == impronta_token(token)


def test_impronta_token_e_sha256():
    import hashlib

    assert impronta_token("abc") == hashlib.sha256(b"abc").hexdigest()
