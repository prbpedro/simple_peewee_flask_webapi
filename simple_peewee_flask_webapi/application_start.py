from flask import Flask
from flask import abort
from flask.json import dumps
from flask.globals import request
from simple_peewee_flask_webapi.app_models import database_proxy
from simple_peewee_flask_webapi.app_models import SimpleTable, JoinTable
from flask.wrappers import Response

app = Flask(__name__)


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

    simple_table = SimpleTable.get(id_simple_table)
    join_dict = {}
    joins = simple_table.joins.execute()
    for i in range(len(joins)):
        join_dict['join_' + str(joins[i].id)] = joins[i].__data__

    join_table = JoinTable.get(id_join_table)
    simple_dict = {'simple_obj': join_table.simple.__data__}

    simple_table_merge = {**simple_table.__data__, **join_dict}
    join_table_merge = {**join_table.__data__, **simple_dict}

    js = dumps({'simple_table': simple_table_merge,
                'join_table': join_table_merge}, default=str)

    return Response(js, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
