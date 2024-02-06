"""Unit test for signup functions"""

from src.auth import (valid_email_format, valid_email_dns,
                      valid_password_format, name_registered, email_registered)


def test_valid_email_format():
    """Tests valid_email_format function"""

    assert valid_email_format("f affav@gmail.com") is False
    assert valid_email_format("javierodriguez@.com") is False
    assert valid_email_format("@gmail.com") is False
    assert valid_email_format(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") is False

    assert valid_email_format("a@gmail.com") is True
    assert valid_email_format("jorge@jorgelin.com") is True


def test_valid_email_dns():
    """Tests valid_email_dns function"""

    assert valid_email_dns("juanpepito@asdasdfghfgha.com") is False
    assert valid_email_dns("juanpepito@gmial.com") is False
    assert valid_email_dns("juanpepito@gmail.com") is True


def test_valid_password_format():
    """Tests valid_password_format"""

    assert valid_password_format("aasfsdvb2A") is False
    assert valid_password_format("s12313124ASs") is False

    assert valid_password_format("Elcolo62$")


def test_name_registered(test_app):
    """Tests name_registered function"""

    assert name_registered("reisch") is False

    assert name_registered("david_musteink")


def test_email_registered(test_app):
    """Tests email_registered function"""

    assert email_registered("mfmariescurrena@gmail.com") is False

    assert email_registered("elcolo@gmail.com")
