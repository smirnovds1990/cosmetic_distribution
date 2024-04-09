from flask_wtf import FlaskForm
from wtforms import (
    FieldList, FormField, IntegerField, SelectField, SelectMultipleField,
    StringField, SubmitField
)
from wtforms.validators import DataRequired, NumberRange, Optional


class ProductForm(FlaskForm):
    title = StringField(
        'Название', validators=[DataRequired(message='Обязательное поле')]
    )
    volume = StringField(
        'Объем', validators=[DataRequired(message='Обязательное поле')]
    )
    amount = IntegerField(
        'Количество',
        validators=[
            DataRequired(message='Обязательное поле'),
            NumberRange(min=0)
        ]
    )
    brand = StringField('Бренд', validators=[Optional()])
    submit = SubmitField('Добавить')


class CustomerForm(FlaskForm):
    name = StringField(
        'Ф. И. О.', validators=[DataRequired(message='Обязательное поле')]
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
        'Цена', validators=[DataRequired(message='Обязательное поле')]
    )
    submit_remove = SubmitField('Удалить')


class OrderForm(FlaskForm):
    customer = SelectField('Клиент', choices=[])
    products = FieldList(
        FormField(OrderProductForm),
        validators=[DataRequired(message='Обязательное поле')],
        min_entries=1
    )
    submit = SubmitField('Добавить')
