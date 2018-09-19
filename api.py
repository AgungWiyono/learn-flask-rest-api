'''
The source is from practicing the tutorial made by Miguel Grinberg.
'''

from flask import Flask, abort, make_response
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal

app = Flask(__name__)
api = Api(app)


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

task_fields = {
        'title': fields.String,
        'detail': fields.String,
        'status': fields.Boolean,
        'uri': fields.Url('task')
        }


class TaskList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   location='json')
        self.reqparse.add_argument('detail', type=str, default="",
                                   location="json")
        super().__init__()

    def get(self):
        task = tasksdata[0]
        return {'tasks':marshal(task, task_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
                'id': tasksdata[-1]['id']+1,
                'title': args['title'],
                'detail': args['detail'],
                'status': False
                }
        tasksdata.append(task)
        return {'task': marshal(task, task_fields)}, 201


class Task(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('detail', type=str, location='json')
        self.reqparse.add_argument('status', type=bool, location='json')
        super().__init__()

    def get(self, id):
        task = [task for task in tasksdata if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task, task_fields)}

    def put(self, id):
        task = [task for task in tasksdata if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for key, value in args.items():
            if value is not None:
                task[key] = value
        return {'task': marshal(task, task_fields)}

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
