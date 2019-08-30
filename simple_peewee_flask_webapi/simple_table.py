from flask import Blueprint
from flask import abort
from flask.json import dumps
from flask.globals import request
from simple_peewee_flask_webapi.app_models import SimpleTable
from flask.wrappers import Response
from peewee import DoesNotExist

simple_table_api = Blueprint('simple_table_api', __name__)


@simple_table_api.route('/simple-table/', methods=['GET', 'POST'])
def get_simple_table():
    id_simple_table = None

    if request.method == 'GET':
        id_simple_table = request.args.get('id_simple_table')
    elif request.method == 'POST':
        id_simple_table = request.form.get('id_simple_table')

    if id_simple_table is None or id_simple_table == "":
        abort(400, 'id_simple_table not informed')

    simple_table = None
    try:
        simple_table = SimpleTable.get(int(id_simple_table))
    except DoesNotExist:
        abort(404, 'simple_table not found')

    join_dict = {}
    joins = simple_table.joins.execute()
    for i in range(len(joins)):
        join_dict['join_' + str(joins[i].id)] = joins[i].__data__

    simple_table_merge = {**simple_table.__data__, **join_dict}

    js = dumps({'simple_table': simple_table_merge}, default=str)

    return Response(js, status=200, mimetype='application/json')
