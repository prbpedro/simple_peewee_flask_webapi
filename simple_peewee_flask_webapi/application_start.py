from flask import Flask
from flask import abort
from flask.json import dumps
from flask.globals import request
from simple_peewee_flask_webapi.app_models import database_proxy
from simple_peewee_flask_webapi.app_models import SimpleTable, JoinTable
from flask.wrappers import Response
from simple_peewee_flask_webapi.simple_table import simple_table_api
from simple_peewee_flask_webapi.join_table import join_table_api
from peewee import DoesNotExist

app = Flask(__name__)
app.register_blueprint(simple_table_api)
app.register_blueprint(join_table_api)


@app.before_request
def before_request():
    database_proxy.connect()


@app.after_request
def after_request(response):
    database_proxy.close()
    return response


@app.route('/get-models/', methods=['GET', 'POST'])
def get_models():
    id_simple_table = None
    id_join_table = None

    if request.method == 'GET':
        id_simple_table = request.args.get('id_simple_table')
        id_join_table = request.args.get('id_join_table')
    elif request.method == 'POST':
        id_simple_table = request.form.get('id_simple_table')
        id_join_table = request.form.get('id_join_table')

    if id_simple_table is None or id_simple_table == "":
        abort(400, 'id_simple_table not informed')

    if id_join_table is None or id_join_table == "":
        abort(400, 'id_join_table not informed')

    simple_table = None
    try:
        simple_table = SimpleTable.get(int(id_simple_table))
    except DoesNotExist:
        abort(404, 'simple_table not found')

    join_dict = {}
    joins = simple_table.joins.execute()
    for i in range(len(joins)):
        join_dict['join_' + str(joins[i].id)] = joins[i].__data__

    join_table = None
    try:
        join_table = JoinTable.get(int(id_join_table))
    except DoesNotExist:
        abort(404, 'join_table not found')

    simple_dict = {'simple_obj': join_table.simple.__data__}

    simple_table_merge = {**simple_table.__data__, **join_dict}
    join_table_merge = {**join_table.__data__, **simple_dict}

    js = dumps({'simple_table': simple_table_merge,
                'join_table': join_table_merge}, default=str)

    return Response(js, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
