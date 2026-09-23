"""Identità dello staff dello studio: sessioni, capacità, password e token.

Nato il 24 settembre 2026 estraendo la parte che il Portale Cedolini e
Fatturazione Studio avevano già duplicata a mano (`core/security.py` era
identico nei due repository, `core/capacita.py`/`core/capabilities.py`
avevano lo stesso meccanismo scritto due volte). Non unifica i database: ogni
programma mantiene la propria tabella utenti e la propria tabella sessioni.
Unifica solo il codice che decide come si autentica una persona, come si
rinnova una sessione e come si verifica una capacità, così una correzione di
sicurezza (come il tetto di sessione mancante nel Portale, trovato proprio
confrontando i due) si scrive una volta sola.

Cosa resta deliberatamente fuori da questo pacchetto: gli enum `Ruolo` e
`Capacita` di ciascun programma (sono elenchi diversi per dominio diverso),
i modelli ORM (schemi diversi, un programma usa UUID e Postgres multi
tenant, l'altro identificativi stringa), e la scrittura vera del registro
delle azioni (le tabelle hanno colonne diverse: qui c'è solo la costante e
la validazione dell'esito, non lo schema della riga).
"""

from __future__ import annotations
