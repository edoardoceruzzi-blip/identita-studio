"""Password e token: le due cose che non si salvano mai in chiaro.

Prima di questo pacchetto, questo file esisteva identico in due posti
(`PortaleCedolini/backend/app/core/security.py` e
`Fatturazione studio/backend/app/core/security.py`), il secondo copiato a
mano dal primo. Non c'è motivo di avere due copie: una correzione di
sicurezza qui vale per entrambi i programmi senza doverla tradurre né
ricordarsi di applicarla due volte.

**Le password e i token si trattano in modo diverso apposta.** Una password
è scelta da una persona, quindi ha poca entropia e va rallentata con un
algoritmo lento (argon2), che rende costoso provarne milioni. Un token è
generato a caso con 256 bit di entropia: provarlo a forza bruta non è un
attacco possibile, quindi basta sha256, che è veloce perché viene calcolato
a ogni richiesta.
"""

from __future__ import annotations

import hashlib
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_cifratore = PasswordHasher()


def cifra_password(password: str) -> str:
    return _cifratore.hash(password)


def verifica_password(password: str, impronta: str) -> bool:
    try:
        return _cifratore.verify(impronta, password)
    except VerifyMismatchError:
        return False
    except Exception:
        # Un hash malformato o scritto con un altro algoritmo si tratta come
        # password sbagliata, mai come eccezione: un'eccezione qui
        # trasformerebbe una riga rovinata nel database in un errore 500 che
        # non dice niente, invece di un accesso negato che si capisce.
        return False


def token_opaco() -> str:
    """Un token casuale ad alta entropia, in forma adatta a un cookie e a un
    URL. Opaco vuol dire che non contiene informazioni: non è un JWT, non
    dice chi sia l'utente, e da solo non vale niente senza la riga
    corrispondente nella tabella delle sessioni."""
    return secrets.token_urlsafe(32)


def impronta_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
