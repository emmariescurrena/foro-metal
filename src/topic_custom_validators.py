"""Custom validators for forms"""

import re
from wtforms import ValidationError
from .main_queries import topic_title_in_table
regex_only_letters_and_hyphens = re.compile(
    r"^(?!-)(?!.*--)[a-z-]{1,30}(?<!-)$")


class UniqueTopicTitle(object):
    """Unique topic name validator"""

    def __init__(self, message=None):
        if not message:
            message = "Ya existe un tópico con este título"
        self.message = message

    def __call__(self, form, field):
        if topic_title_in_table(field.data):
            raise ValidationError(self.message)


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

    if _min <= number <= _max:
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

    return True if re.fullmatch(regex_only_letters_and_hyphens, string) else False


def invalid_tags(arr):
    """Returns True if arr has invalid tags"""

    for word in arr:
        if has_only_letters_and_hyphens(word) is False:
            return True


class TagsValidCharacters(object):
    """Tags valid characters validator"""

    def __init__(self, message=None):
        if not message:
            message = """Las etiquetas deben contener letras minúsculas sin
            tildes, guiones para separar entre diferentes palabras en la misma
            etiqueta, no puede haber dos guiones consecutivos y no pueden
            empezar ni terminar en guiones"""
        self.message = message

    def __call__(self, form, field):
        tag_names = field.data.split()
        if invalid_tags(tag_names):
            raise ValidationError(self.message)
