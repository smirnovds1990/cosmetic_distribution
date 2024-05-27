from flask_wtf import FlaskForm
from wtforms import (
    FieldList, FloatField, FormField, IntegerField, SelectField, StringField,
    SubmitField
)
from wtforms.validators import (
    DataRequired, NumberRange, Optional, Regexp, ValidationError
)

from .constants import NAME_PATTERN
from .validators import price_is_positive, product_quantity_is_enough


class ProductForm(FlaskForm):
    title = StringField(
        'Название', validators=[DataRequired(message='Обязательное поле')]
    )
    amount = IntegerField(
        'Количество',
        validators=[
            DataRequired(message='Обязательное поле'),
            NumberRange(min=1)
        ]
    )
    brand = StringField('Бренд', validators=[Optional()])
    wholesale_price = FloatField(
        'Закупочная цена', validators=[
            DataRequired(message='Обязательное поле'),
            price_is_positive
        ]
    )
    retail_price = FloatField(
        'Розничная цена', validators=[
            DataRequired(message='Обязательное поле'),
            price_is_positive
        ]
    )
    submit = SubmitField('Добавить')

    def validate_retail_price(self, field):
        if field.data <= self.wholesale_price.data:
            raise ValidationError(
                'Розничная цена не может быть меньше закупочной.'
            )


class CustomerForm(FlaskForm):
    name = StringField(
        'Ф. И. О.',
        validators=[
            DataRequired(message='Обязательное поле'),
            Regexp(
                NAME_PATTERN,
                message='В имени можно использовать только русские буквы.'
            )
        ]
    )
    submit = SubmitField('Добавить')


class OrderProductForm(FlaskForm):
    products = SelectField(
        'Товары',
        choices=[],
        validators=[DataRequired(message='Обязательное поле')]
    )
    quantity = IntegerField(
        'Количество', validators=[
            DataRequired(message='Обязательное поле'),
            NumberRange(min=1)
        ]
    )
    price = IntegerField(
        'Цена', validators=[
            DataRequired(message='Обязательное поле'),
            NumberRange(min=1)
        ]
    )


class OrderForm(FlaskForm):
    customer = SelectField('Клиент', choices=[])
    products = FieldList(
        FormField(OrderProductForm),
        validators=[
            DataRequired(message='Обязательное поле'),
            product_quantity_is_enough
        ],
        min_entries=1
    )
    submit = SubmitField('Добавить')
