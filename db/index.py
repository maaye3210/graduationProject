from peewee import *

database = MySQLDatabase('navigation', **{
    'charset': 'utf8',
    'sql_mode': 'PIPES_AS_CONCAT',
    'use_unicode': True,
    'host': '1.13.190.26',
    'user': 'root',
    'password': 'may387951992'
})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Modal(BaseModel):
    a = FloatField(column_name='A', null=True)
    c_d = DecimalField(column_name='C_D', null=True)
    delta = FloatField(null=True)
    eta_t = DecimalField(column_name='eta_T', null=True)
    eta_b = DecimalField(null=True)
    eta_c = DecimalField(null=True)
    eta_m = DecimalField(null=True)
    f = DecimalField(null=True)
    k = DecimalField(null=True)
    m = IntegerField()
    name = CharField()

    class Meta:
        table_name = 'modal'


modals = Modal.select()

for modal in modals:
    print(modal)