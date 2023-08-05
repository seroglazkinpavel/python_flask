"""
Необходимо создать базу данных для интернет-магазина. База данных должна
состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
содержать информацию о доступных товарах, их описаниях и ценах. Таблица
пользователи должна содержать информацию о зарегистрированных
пользователях магазина. Таблица заказы должна содержать информацию о
заказах, сделанных пользователями.
○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
имя, фамилия, адрес электронной почты и пароль.
○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
название, описание и цена.
○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
заказа.
Создайте модели pydantic для получения новых данных и
возврата существующих в БД для каждой из трёх таблиц
(итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через
создание маршрутов, REST API (итого 15 маршрутов).
○ Чтение всех
○ Чтение одного
○ Запись
○ Изменение
○ Удаление
"""

import databases
import sqlalchemy
from datetime import datetime, date, timedelta
from pydantic import BaseModel, Field
from fastapi import FastAPI, Path, HTTPException
from typing import List
from random import randint, choice


DATABASE_URL = "sqlite:///homework_6/internet_shop.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(300)),
    sqlalchemy.Column("price", sqlalchemy.Integer)
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("prod_id", sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String(20))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class User(BaseModel):
    id: int = Field(default=None)
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=5, max_length=120)


class UserIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    surname: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=5, max_length=120)


class Products(BaseModel):
    id: int = Field(default=None)
    name: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=2, max_length=200)
    price: float = Field(..., ge=0.1, le=100000)


class ProductsIn(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=2, max_length=200)
    price: float = Field(..., ge=0.1, le=100000)


class Order(BaseModel):
    id: int = Field(default=None)
    user_id: int
    prod_id: int
    order_date: date = Field(default=datetime.now())
    status: str = Field(default='in_progress')


class OrderIn(BaseModel):
    user_id: int
    prod_id: int
    order_date: date = Field(default=datetime.now())
    status: str = Field(default='in_progress')


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def root():
    return {"Message": "Hello"}


@app.get('/fake_users/{count}')
async def create_users(count: int):
    for i in range(count):
        query = users.insert().values(name=f'user{i}',
                                      surname=f'surname{i}',
                                      email=f'shop{i}@bk.ru',
                                      password=f'zxcvbnm{i}')
        await database.execute(query)
    return {'message': f'{count} fake users create'}


@app.get('/fake_products/{count}')
async def create_products(count: int):
    for i in range(count):
        query = products.insert().values(
            name=f'Name_products {i}',
            description='Product description',
            price=f'{randint(1, 100000)}'
        )
        await database.execute(query)
    return {'message': f'{count} fake products create'}


@app.get('/fake_orders/{count}')
async def create_orders(count: int):
    for i in range(count):
        query = orders.insert().values(
            user_id=randint(1, 10),
            prod_id=randint(1, 10),
            order_date=datetime.strptime("2021-01-24", "%Y-%m-%d").date() + timedelta(days=i ** 2),
            status=choice(['in_progress', 'created', 'cancelled'])
        )
        await database.execute(query)
    return {'message': f'{count} fake orders create'}


@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int = Path(..., ge=1)):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password
        )
    actual_id = await database.execute(query)
    return {**user.dict(), 'id': actual_id}


@app.put('/users/{user_id}', response_model=User)
async def update_user(new_user: UserIn, user_id: int = Path(..., ge=1)):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), 'id': user_id}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(..., ge=1)):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': f'User with id {user_id} was deleted'}


@app.get('/products/', response_model=List[Products])
async def get_all_products():
    query = products.select()
    return await database.fetch_all(query)



@app.get('/products/{product_id}', response_model=Products)
async def get_product(product_id: int = Path(..., ge=1)):
    query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post('/products/', response_model=Products)
async def create_product(product: ProductsIn):
    query = products.insert().values(
        name=product.name,
        description=product.description,
        price=product.price
        )
    actual_id = await database.execute(query)
    return {**product.dict(), 'id': actual_id}


@app.put('/products/{product_id}', response_model=Products)
async def update_product(new_product: ProductsIn, product_id: int = Path(..., ge=1)):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), 'id': product_id}


@app.delete('/products/{product_id}')
async def delete_product(product_id: int = Path(..., ge=1)):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': f'User with id {product_id} was deleted'}


@app.get('/orders/', response_model=List[Order])
async def get_all_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get('/orders/{order_id}', response_model=Order)
async def get_order(order_id: int = Path(..., ge=1)):
    query = orders.select().where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(
        order_date=order.order_date,
        status=order.status,
        user_id=order.user_id,
        prod_id=order.prod_id
        )
    actual_id = await database.execute(query)
    return {**order.dict(), 'id': actual_id}


@app.put('/orders/{order_id}', response_model=Order)
async def update_order(new_order: OrderIn, order_id: int = Path(..., ge=1)):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), 'id': order_id}


@app.delete('/orders/{order_id}')
async def delete_order(order_id: int = Path(..., ge=1)):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': f'User with id {order_id} was deleted'}