from wtforms.validators import ValidationError

from .constants import NAME_PATTERN
from .models import Product


def only_russian_chars(form, field):
    if field.data not in NAME_PATTERN:
        raise ValidationError(
            'В имени можно использовать только русские буквы.'
        )


def product_quantity_is_enough(form, field):
    products_data = [
        (
            product['products'],
            product['quantity']
        ) for product in field.data
    ]
    products_in_deficit = []
    for item in products_data:
        product = Product.query.filter_by(id=item[0]).first_or_404()
        available_amount = product.amount
        if available_amount < item[1]:
            products_in_deficit.append(product.title)
    if products_in_deficit:
        raise ValidationError(
            f'В наличии нет достаточного количества следующих товаров:\n'
            f'{products_in_deficit}'
        )


def price_is_positive(form, field):
    if field.data is None:
        raise ValidationError('В цене можно использовать только цифры.')
    elif field.data < 0:
        raise ValidationError('Цена не может быть меньше 0.')
