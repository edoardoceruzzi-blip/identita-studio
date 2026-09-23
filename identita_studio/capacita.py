"""Il meccanismo dell'autorizzazione per capacità, non l'elenco delle capacità.

Portale Cedolini e Fatturazione Studio hanno ciascuno il proprio enum
`Ruolo`, il proprio enum `Capacita` e la propria mappa `CAPACITA_PER_RUOLO`:
sono elenchi diversi per domini diversi (chi carica cedolini non è lo stesso
mestiere di chi emette una fattura) e restano locali a ciascun programma,
qui non ci sono.

Quello che i due programmi avevano già uguale, scritto due volte a mano, è
il meccanismo che applica quella mappa: un ruolo assente nega tutto invece
di concedere tutto (il default sicuro), e una rotta protetta chiede una
capacità, mai un ruolo, così aggiungere un ruolo nuovo costa una riga nella
mappa e non una modifica a ogni endpoint. Quel meccanismo vive qui, una
volta sola.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import TypeVar

from fastapi import Depends, HTTPException, status

RuoloT = TypeVar("RuoloT")
CapacitaT = TypeVar("CapacitaT")
UtenteT = TypeVar("UtenteT")


def capacita_di(
    ruolo: RuoloT, mappa: Mapping[RuoloT, frozenset[CapacitaT]]
) -> frozenset[CapacitaT]:
    """Le capacità di un ruolo. Un ruolo assente dalla mappa non ne ha
    nessuna: è il default sicuro, così un valore aggiunto all'enum senza la
    riga corrispondente nella mappa nega tutto invece di concedere tutto."""
    return mappa.get(ruolo, frozenset())


def ha_capacita(
    ruolo: RuoloT,
    capacita: CapacitaT,
    mappa: Mapping[RuoloT, frozenset[CapacitaT]],
) -> bool:
    return capacita in capacita_di(ruolo, mappa)


def richiede_capacita(
    capacita: CapacitaT,
    *,
    mappa: Mapping[RuoloT, frozenset[CapacitaT]],
    ottieni_ruolo: Callable[[UtenteT], RuoloT],
    ottieni_utente_corrente: Callable[..., UtenteT],
) -> Callable[..., UtenteT]:
    """Costruisce una dependency FastAPI che ammette solo chi ha questa
    capacità.

    `ottieni_ruolo` traduce l'utente della sessione nel suo `Ruolo` (nel
    Portale è un campo diretto sul modello, in Fatturazione passa da
    `core.utenti.ruolo_di` perché il ruolo è salvato come stringa). Il
    messaggio di errore resta generico di proposito: dire quale capacità
    manca descriverebbe a un utente non autorizzato la struttura interna dei
    permessi, e non gli servirebbe comunque a niente.
    """

    def dipendenza(utente: UtenteT = Depends(ottieni_utente_corrente)) -> UtenteT:
        if not ha_capacita(ottieni_ruolo(utente), capacita, mappa):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Operazione non consentita")
        return utente

    return dipendenza
