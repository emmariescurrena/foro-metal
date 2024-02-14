"""Custom validators for forms"""

import re
from wtforms import ValidationError

regex_only_letters_and_hyphens = re.compile(
    r"/^(?!-)(?!.*--)[a-z-]{1,30}(?<!-)$")


def words_quantity(string):
    """
    Returns string's words quantity
    Returns an int
    """

    return len(string.split())


def valid_words_quantity_range(number, _min, _max):
    """
    Returns True if number is equal or above min and is
    equal or below max, else False
    """

    if number >= _min and number <= _max:
        return True
    return False


class TagsQuantity(object):
    """Tags quantity validator"""

    def __init__(self, message=None):
        if not message:
            message = "Debes ingresar como mínimo 1 etiqueta y como máximo 5"
        self.message = message

    def __call__(self, form, field):
        words = words_quantity(field.data)
        if not valid_words_quantity_range(words, 1, 5):
            raise ValidationError(self.message)


def has_only_letters_and_hyphens(string):
    """Returns True if string has only letters and hyphens"""

    arr = string.split()

    for word in arr:
        if not re.fullmatch(regex_only_letters_and_hyphens, word):
            return False
    return True


class TagsValidCharacters(object):
    """Tags quantity validator"""

    def __init__(self, message=None):
        if not message:
            message = """Las etiquetas deben contener letras minúsculas sin
            tildes, guiones para separar entre diferentes palabras en la misma
            etiqueta, no puede haber dos guinoes consecutivos y no pueden
            empezar ni terminar en guiones"""
        self.message = message

    def __call__(self, form, field):
        if not has_only_letters_and_hyphens(field.data):
            raise ValidationError(self.message)
