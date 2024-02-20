"""Custom validators for signup form"""

import re
from wtforms import ValidationError
from pyisemail import is_email
from .models import User

regex_email = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")  # pylint: disable=line-too-long
regex_password = re.compile(
    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")


def name_registered(name):
    """Returns True if name is registered, else False"""

    return True if User.query.filter_by(name=name).first() else False


class NameRegistered(object):
    """Name registered validator"""

    def __init__(self, message=None):
        if not message:
            message = "Nombre de usuario ya registrado"
        self.message = message

    def __call__(self, form, field):
        if name_registered(field.data):
            raise ValidationError(self.message)


def email_registered(email):
    """Returns True if email is registered, else False"""

    return True if User.query.filter_by(email=email).first() else False


class EmailRegistered(object):
    """Email registered validator"""

    def __init__(self, message=None):
        if not message:
            message = "Correo electrónico ya registrado"
        self.message = message

    def __call__(self, form, field):
        if email_registered(field.data):
            raise ValidationError(self.message)


def valid_email_format(string):
    """Returns True if string has valid email format, else False"""

    if re.fullmatch(regex_email, string) and is_email(string):
        return True
    return False


class ValidEmailFormat(object):
    """Valid email format validator"""

    def __init__(self, message=None):
        if not message:
            message = "El formato del correo electrónico es inválido"
        self.message = message

    def __call__(self, form, field):
        if not valid_email_format(field.data):
            raise ValidationError(self.message)


class NameNotEmail(object):
    """Name not email validator"""

    def __init__(self, message=None):
        if not message:
            message = "El nombre de usuario no debe ser un correo electrónico"
        self.message = message

    def __call__(self, form, field):
        if valid_email_format(field.data):
            raise ValidationError(self.message)


def valid_email_dns(email):
    """Returns True if email has a valid domain, else False"""

    return True if is_email(email, check_dns=True) else False


class ValidEmailDns(object):
    """Valid email dns validator"""

    def __init__(self, message=None):
        if not message:
            message = "El dominio del correo electrónico es inválido"
        self.message = message

    def __call__(self, form, field):
        if not valid_email_dns(field.data):
            raise ValidationError(self.message)


def valid_password_format(password):
    """Returns True if password match regex, else False"""

    return True if re.fullmatch(regex_password, password) else False


class ValidPasswordFormat(object):
    """Valid password format validator"""

    def __init__(self, message=None):
        if not message:
            message = "El formato de la contraseña es inválido"
        self.message = message

    def __call__(self, form, field):
        if not valid_password_format(field.data):
            raise ValidationError(self.message)
