# Приложение для учёта складских остатков и продажи товаров.


Приложение создано для улучшения контроля складских остатков и продаж в небольших объёмах (К примеру для салонов красоты).
Администратор, управляя складскими остатками, добавляет товары на склад и, при продаже, создаёт заказ под определённого клиента (который предварительно тоже создаётся).
В данный момент реализовано MVP, в будущем планируется расширение приложения с добавлением возможности удобного и быстрого сбора аналитики как по складу так и по заказам, расширение профиля заказчика, автоматизированное формирование ценников для товаров.


#### Технологии

- Python
- Flask
- SQLAlchemy
- Alembic
- HTML
- SQLite


#### Установка
Скачать репозиторий, установить и активировать виртуальное окружение
```sh
https://github.com/smirnovds1990/cosmetic_distribution
python -m venv venv (для Unix 'python3')
(Windows) source venv/Scripts/activate
(Unix) source venv/bin/activate
```


Установить зависимости, сделать миграции
```sh
pip install --upgrade pip
pip install -r requirements.txt
flask db upgarde
```
Создать пользователя-администратора
```sh
flask shell
from cosmetic_distribution import db
from cosmetic_distribution.models import User
from werkzeug.security import generate_password_hash
hashed_password = generate_password_hash('YourPassword')
new_user = User(username='YourUser', password=hashed_password)
db.session.add(new_user)
db.session.commit()
```
Запустить приложение
```sh
flask run
```
Перейти http://127.0.0.1:5000

###### Автор: [https://github.com/smirnovds1990](https://github.com/smirnovds1990)
