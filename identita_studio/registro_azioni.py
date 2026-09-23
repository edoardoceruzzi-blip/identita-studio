"""Solo la costante e la validazione dell'esito, non la riga di registro.

Le due tabelle sono diverse per costruzione: `AzioneAmministrativa` del
Portale registra solo le operazioni distruttive (cancella_documento,
cancella_dipendente, cancella_tenant), `AzioneRiga` di Fatturazione registra
ogni azione, inclusi i tentativi falliti con indirizzo IP. Forzarle nello
stesso schema qui dentro imporrebbe una forma finta a uno dei due, quindi lo
schema resta locale a ciascun programma. Quello che si condivide è la sola
cosa davvero identica: i due esiti ammessi, e il fatto che un esito diverso
da questi due è un errore di programmazione, non un caso da gestire.
"""

from __future__ import annotations

RIUSCITA = "riuscita"
RIFIUTATA = "rifiutata"

ESITI_VALIDI = frozenset({RIUSCITA, RIFIUTATA})


def valida_esito(esito: str) -> None:
    if esito not in ESITI_VALIDI:
        raise ValueError(f"esito sconosciuto: {esito!r}")
