from datetime import datetime, timedelta, timezone

from identita_studio.sessioni import DURATA_MASSIMA_ORE_DEFAULT, calcola_nuova_scadenza


def test_rinnovo_normale_si_allontana():
    creata_il = datetime(2026, 1, 1, tzinfo=timezone.utc)
    adesso = creata_il + timedelta(hours=2)
    nuova = calcola_nuova_scadenza(adesso=adesso, creata_il=creata_il, ore_rinnovo=12)
    assert nuova == adesso + timedelta(hours=12)


def test_rinnovo_oltre_il_tetto_si_ferma_al_tetto():
    creata_il = datetime(2026, 1, 1, tzinfo=timezone.utc)
    tetto_ore = 24  # tetto breve per rendere il test leggibile
    adesso = creata_il + timedelta(hours=23)
    nuova = calcola_nuova_scadenza(
        adesso=adesso, creata_il=creata_il, ore_rinnovo=12, ore_tetto=tetto_ore
    )
    assert nuova == creata_il + timedelta(hours=tetto_ore)


def test_rinnovo_prima_del_tetto_non_lo_tocca():
    creata_il = datetime(2026, 1, 1, tzinfo=timezone.utc)
    tetto_ore = 24
    adesso = creata_il + timedelta(hours=1)
    nuova = calcola_nuova_scadenza(
        adesso=adesso, creata_il=creata_il, ore_rinnovo=2, ore_tetto=tetto_ore
    )
    assert nuova == adesso + timedelta(hours=2)
    assert nuova < creata_il + timedelta(hours=tetto_ore)


def test_default_e_una_settimana():
    assert DURATA_MASSIMA_ORE_DEFAULT == 24 * 7


def test_sessione_usata_di_continuo_non_vive_per_sempre():
    creata_il = datetime(2026, 1, 1, tzinfo=timezone.utc)
    adesso = creata_il
    for _ in range(1000):
        adesso = adesso + timedelta(hours=1)
        nuova = calcola_nuova_scadenza(adesso=adesso, creata_il=creata_il, ore_rinnovo=12)
        assert nuova <= creata_il + timedelta(hours=DURATA_MASSIMA_ORE_DEFAULT)
