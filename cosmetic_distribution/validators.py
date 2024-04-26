from wtforms.validators import ValidationError

from .constants import NAME_PATTERN


def only_russian_chars(form, field):
    if field.data not in NAME_PATTERN:
        raise ValidationError(
            'В имени можно использовать только русские буквы.'
        )
