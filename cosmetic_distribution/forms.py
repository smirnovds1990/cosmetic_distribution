from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
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
