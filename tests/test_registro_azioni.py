import pytest

from identita_studio.registro_azioni import RIFIUTATA, RIUSCITA, valida_esito


def test_esiti_validi_non_sollevano():
    valida_esito(RIUSCITA)
    valida_esito(RIFIUTATA)


def test_esito_sconosciuto_solleva():
    with pytest.raises(ValueError):
        valida_esito("boh")
