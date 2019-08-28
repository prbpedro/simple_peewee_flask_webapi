from flask import Blueprint
from flask import abort
from flask.json import dumps
from flask.globals import request
from simple_peewee_flask_webapi.app_models import JoinTable
from flask.wrappers import Response
from peewee import DoesNotExist

join_table_api = Blueprint('join_table_api', __name__)


@join_table_api.route('/join_table/', methods=['GET', 'POST'])
def get_models():
    id_join_table = None

    if request.method == 'GET':
        id_join_table = request.args.get('id_join_table')
    elif request.method == 'POST':
        id_join_table = request.form.get('id_join_table')

    if id_join_table is None or id_join_table == "":
        abort(400, 'id_join_table not informed')

    join_table = None
    try:
        join_table = JoinTable.get(int(id_join_table))
    except DoesNotExist:
        abort(404, 'join_table not found')

    simple_dict = {'simple_obj': join_table.simple.__data__}
    join_table_merge = {**join_table.__data__, **simple_dict}

    js = dumps({'join_table': join_table_merge}, default=str)

    return Response(js, status=200, mimetype='application/json')
