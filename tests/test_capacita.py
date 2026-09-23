import enum

import pytest
from fastapi import HTTPException

from identita_studio.capacita import capacita_di, ha_capacita, richiede_capacita


class Ruolo(str, enum.Enum):
    ADMIN = "admin"
    OPERATORE = "operatore"


class Capacita(str, enum.Enum):
    LEGGI = "leggi"
    SCRIVI = "scrivi"


MAPPA: dict[Ruolo, frozenset[Capacita]] = {
    Ruolo.ADMIN: frozenset({Capacita.LEGGI, Capacita.SCRIVI}),
    Ruolo.OPERATORE: frozenset({Capacita.LEGGI}),
}


def test_capacita_di_ruolo_presente():
    assert capacita_di(Ruolo.OPERATORE, MAPPA) == frozenset({Capacita.LEGGI})


def test_capacita_di_ruolo_assente_e_vuoto():
    # Un ruolo che esiste nell'enum ma non e' stato aggiunto alla mappa (caso
    # tipico: un ruolo nuovo dimenticato) non ha nessuna capacita', mai tutte.
    class RuoloExtra(str, enum.Enum):
        OSPITE = "ospite"

    assert capacita_di(RuoloExtra.OSPITE, MAPPA) == frozenset()


def test_ha_capacita_vero_e_falso():
    assert ha_capacita(Ruolo.ADMIN, Capacita.SCRIVI, MAPPA)
    assert not ha_capacita(Ruolo.OPERATORE, Capacita.SCRIVI, MAPPA)


class UtenteFinto:
    def __init__(self, ruolo: Ruolo):
        self.ruolo = ruolo


def test_richiede_capacita_ammette_chi_ce_lha():
    dipendenza = richiede_capacita(
        Capacita.SCRIVI,
        mappa=MAPPA,
        ottieni_ruolo=lambda u: u.ruolo,
        ottieni_utente_corrente=lambda: UtenteFinto(Ruolo.ADMIN),
    )
    utente = UtenteFinto(Ruolo.ADMIN)
    assert dipendenza(utente) is utente


def test_richiede_capacita_rifiuta_chi_non_ce_lha():
    dipendenza = richiede_capacita(
        Capacita.SCRIVI,
        mappa=MAPPA,
        ottieni_ruolo=lambda u: u.ruolo,
        ottieni_utente_corrente=lambda: UtenteFinto(Ruolo.OPERATORE),
    )
    with pytest.raises(HTTPException) as errore:
        dipendenza(UtenteFinto(Ruolo.OPERATORE))
    assert errore.value.status_code == 403
