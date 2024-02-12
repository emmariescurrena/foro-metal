"""Custom validators for forms"""

import re
from wtforms import ValidationError
from pyisemail import is_email
from .models import User

regex_email = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")  # pylint: disable=line-too-long
regex_password = re.compile(
    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")


class NameRegistered(object):
    """Name registered validator"""

    def __init__(self, message=None):
        if not message:
            message = "El nombre de usuario ya registrado"
        self.message = message

    def __call__(self, form, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError(self.message)


class EmailRegistered(object):
    """Email registered validator"""

    def __init__(self, message=None):
        if not message:
            message = "El correo electrónico ya registrado"
        self.message = message

    def __call__(self, form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(self.message)


class ValidEmailFormat(object):
    """Valid email format validator"""

    def __init__(self, message=None):
        if not message:
            message = "El formato del correo electrónico es inválido"
        self.message = message

    def __call__(self, form, field):
        if not re.fullmatch(regex_email, field.data) and not is_email(field.data):
            raise ValidationError(self.message)


class NameNotEmail(object):
    """Name not email validator"""

    def __init__(self, message=None):
        if not message:
            message = "El nombre de usuario no debe ser un correo electrónico"
        self.message = message

    def __call__(self, form, field):
        if re.fullmatch(regex_email, field.data) and not is_email(field.data):
            raise ValidationError(self.message)


class ValidEmailDns(object):
    """Valid email dns validator"""

    def __init__(self, message=None):
        if not message:
            message = "El dominio del correo electrónico es inválido"
        self.message = message

    def __call__(self, form, field):
        if not is_email(field.data, check_dns=True):
            raise ValidationError(self.message)


class ValidPasswordFormat(object):
    """Valid password format"""

    def __init__(self, message=None):
        if not message:
            message = "El formato de la contraseña es inválido"
        self.message = message

    def __call__(self, form, field):
        if not re.fullmatch(regex_password, field.data):
            raise ValidationError(self.message)
