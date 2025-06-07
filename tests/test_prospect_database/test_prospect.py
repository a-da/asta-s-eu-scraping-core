from asta_s_eu.scraping.core.prospect_database import Prospect


def test_equality():
    """
    GIVEN two prospects
    WHEN compare them
    THEN they have to be equal
    """
    prospect = dict(  # pylint: disable=use-dict-literal
        location='13507 Reinickendorf',
        product_id='2447222860',
        price='10 €',
        text='Philips Filter hu4102 f. Luftbefeuchter 2000er',
        link="...",
        date='Gestern, 16:43',
        tag_list=["Direkt kaufen"]
    )

    prospect1 = Prospect(prospect)
    prospect2 = Prospect(**prospect)

    assert prospect1.to_print() == prospect2.to_print()


def test_hash():
    """
    GIVEN one prospects object
    WHEN include it in to a set
    THEN check if the same prospect is in the set
    """
    prospect1 = Prospect(
        location='13507 Reinickendorf',
        product_id='2447222860',
        price='10 €',
        text='Philips Filter hu4102 f. Luftbefeuchter 2000er',
        link="...",
        date='Gestern, 16:43',
        tag_list=["Direkt kaufen"]
    )
    assert prospect1 in {prospect1, }
