'''
This file is the revision from api.py.
As some reqparse, fields, and marshal feature were deperecated,
the availabale choice using flask-marshmallow to do serialization.
This file is intended on learning about how to use the feature
from flask-marshmallow.
'''

from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)
ma = Marshmallow()


@app.errorhandler(404)
def not_found(error):
    return make_response({'error': 'Not Found'}, 404)


tasksdata = [
                {
                    'id': 1,
                    'title': 'Learn Python API',
                    'status': False,
                    'detail': 'Search Python restful article'
                },
                {
                    'id': 2,
                    'title': 'Build REST API',
                    'status': False,
                    'detail': 'Build REST API with flask-restful'
                }
              ]


class taskSchema(ma.Schema):
    url = ma.URLFor('task', id='<id>')
    title = ma.String(required=True)
    status = ma.Boolean(default=False)
    detail = ma.String(default='')


taskschema = taskSchema()


class TaskList(Resource):
    def get(self):
        return jsonify({'data': [taskschema.dump(task).data for task in
                                 tasksdata]})

    def post(self):
        rawdata = request.get_json(force=True)
        if not rawdata:
            abort(404)
        if rawdata.get('status', False) is True:
            abort(400)
        data, error = taskschema.load(rawdata)
        if error:
            return error, 422
        data['id'] = tasksdata[-1]['id'] + 1
        data['status'] = False
        tasksdata.append(data)
        return jsonify({'data': taskschema.dump(data).data})


class Task(Resource):
    def get(self, id):
        task = [task for task in tasksdata if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return jsonify({'task': taskschema.dump(task[0]).data})

    def put(self, id):
        task = [task for task in tasksdata if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = request.get_json()
        for key in args:
            task[key] = args[key]
        return jsonify({'task': taskschema.dump(task).data})

    def delete(self, id):
        task = [task for task in tasksdata if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasksdata.remove(task[0])
        return {'status': 'Success'}


api.add_resource(TaskList, '/tasks', endpoint='tasks')
api.add_resource(Task, '/tasks/<int:id>', endpoint='task')


if __name__ == '__main__':
    app.run(debug=True)
