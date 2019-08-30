from peewee import Model, AutoField, CharField, DateTimeField, SqliteDatabase
from peewee import IntegrityError
from peewee import ForeignKeyField, DatabaseProxy, OperationalError
import datetime

database_proxy = DatabaseProxy()


class BaseModel(Model):

    class Meta:
        database = database_proxy


class SimpleTable(BaseModel):
    id = AutoField()
    code = CharField(unique=True, max_length=50)


class JoinTable(BaseModel):
    id = AutoField()
    code = CharField(unique=True, max_length=50)
    creation_time = DateTimeField(default=datetime.datetime.now)
    simple = ForeignKeyField(SimpleTable, backref='joins')

# ==============================================================================
# if app.config['DEBUG']:
#     database = SqliteDatabase('local.db')
# elif app.config['TESTING']:
#     database = SqliteDatabase(':memory:')
# else:
#     database = PostgresqlDatabase('mega_production_db')
# ==============================================================================


database_proxy.initialize(SqliteDatabase(
    'simple_flask_peewee_db.db'))

id_simple_table = None
try:
    SimpleTable.create_table()
    id_simple_table = SimpleTable.insert({SimpleTable.code: 'CODE'}).execute()
except OperationalError:
    print('SimpleTable alredy exists')
except IntegrityError:
    id_simple_table = SimpleTable.select().where(
        SimpleTable.code == 'CODE').execute()[0].id

id_join_table = None
try:
    JoinTable.create_table()
    id_join_table = JoinTable.insert({
        JoinTable.code: "CODE",
        JoinTable.simple: id_simple_table}).execute()
except OperationalError:
    print('JoinTable alredy exists')
except IntegrityError:
    id_join_table = JoinTable.select().where(
        JoinTable.code == 'CODE').execute()[0].id

database_proxy.close()
