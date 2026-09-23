"""Il calcolo del rinnovo scorrevole con un tetto, non la tabella.

Ogni programma tiene la propria riga di sessione (colonne e chiave primaria
diverse fra Portale e Fatturazione), quindi qui non c'è un modello ORM: solo
la funzione pura che decide la nuova scadenza, dato quando la sessione è
nata e quando è stata usata l'ultima volta.

**Perché esiste come funzione a sé.** Prima di questo pacchetto Fatturazione
aveva il tetto, il Portale no: il rinnovo lì si allontanava a ogni
richiesta senza mai fermarsi, quindi una sessione usata di continuo non
scadeva mai. È stato trovato confrontando i due programmi per unificarli,
non cercato apposta. Il rinnovo scorrevole serve a non buttare fuori chi sta
lavorando; da solo però fa vivere una sessione per sempre, ed è il motivo
per cui un token rubato e usato ogni giorno non scadrebbe mai senza un
tetto. Il tetto si misura dalla nascita della sessione, non dall'ultimo uso.
"""

from __future__ import annotations

from datetime import datetime, timedelta

DURATA_MASSIMA_ORE_DEFAULT = 24 * 7
"""Una settimana. Oltre questo tetto una sessione scade comunque, anche se
usata di continuo: chi lavora si ripassa dalla password una volta ogni
tanto."""


def calcola_nuova_scadenza(
    *,
    adesso: datetime,
    creata_il: datetime,
    ore_rinnovo: int,
    ore_tetto: int = DURATA_MASSIMA_ORE_DEFAULT,
) -> datetime:
    """La prossima scadenza di una sessione valida, dopo una richiesta.

    Questa funzione non guarda la scadenza attuale della riga: chi chiama
    passa `adesso`, e il risultato non supera mai `creata_il + ore_tetto`.
    """
    tetto = creata_il + timedelta(hours=ore_tetto)
    return min(adesso + timedelta(hours=ore_rinnovo), tetto)
