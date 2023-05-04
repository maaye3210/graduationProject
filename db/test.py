from peewee import MySQLDatabase, Model, DateField, IntegerField, CharField

db_info = {
    'host': '1.13.190.26',
    'port': 3306,
    'db': 'navigation',
    'user': 'root',
    'password': 'may387951992',
    'charset': 'utf8',
}

database = MySQLDatabase('test', **db_info)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    birthday = DateField()
    is_relative = IntegerField()
    name = CharField()

    class Meta:
        table_name = 'person'
