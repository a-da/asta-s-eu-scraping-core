from unittest import mock

from asta_s_eu.scraping.core import send_email


def test_gmailing_prospects():
    """
    GIVEN am extracted data with a few prospects
    WHEN send the email with that data
    THEN prospected rendered into html are sent via email
    """
    prospects = [
        {
            "link": "",
            "price": "100 Euro",
            "text": "product title 1",
            "img": "https://i.ebayimg.com/00/s/ODM4WDE2MDA=/z/nW4AAOSwqMxfhHp1/$_2.JPG",
        },
        {
            "link": "",
            "price": "100 Euro",
            "text": "product title 1",
            "img": "https://i.ebayimg.com/00/s/ODc5WDcyMA==/z/YmwAAOSw9Jxgeb8J/$_2.JPG",
        },
        {
            "link": "",
            "price": "100 Euro",
            "text": "product title 1",
            # "img": "https://i.ebayimg.com/00/s/MTIwMFgxNjAw/z/vtMAAOSwWOBhZzVQ/$_2.JPG",
        },
        {
            "link": "",
            "price": "100 Euro",
            "text": "product title 1",
            "img": "https://i.ebayimg.com/00/s/NjQwWDM2MA==/z/SAsAAOSwQAlhhlsw/$_2.PNG",
        }
    ] * 2

    with mock.patch.object(send_email, "send_any_email") as send_any_email:
        send_email.gmailing_prospects(
            from_="from@mock.web.domain",
            to="to@@mock.web.domain",
            subject="mock subject",
            password="mock-password",
            prospects=prospects
        )
    send_any_email.assert_called_once()

    email = send_any_email.call_args.args[0]
    assert email.html
