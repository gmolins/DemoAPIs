from flask import Flask, request, jsonify, g
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

# Simulación de base de datos en memoria con datos iniciales
tasks = [
    {"id": 1, "title": "Comprar leche", "done": False},
    {"id": 2, "title": "Aprender Flask", "done": True},
    {"id": 3, "title": "Hacer ejercicio", "done": False}
]

def find_task(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)

def validate_task_data(data):
    if "title" not in data:
        abort(400, message="Title is required")

@app.before_request
def before_request():
    g.request_ip = request.remote_addr
    print(f"Request received from {g.request_ip}")

@app.after_request
def after_request(response):
    response.headers["X-Processed-By"] = "Flask API"
    return response

class TaskList(Resource):
    def get(self):
        return jsonify(tasks)
    
    def post(self):
        data = request.get_json()
        validate_task_data(data)
        new_task = {
            "id": len(tasks) + 1,
            "title": data.get("title"),
            "done": False
        }
        tasks.append(new_task)
        return jsonify(new_task), 201

class Task(Resource):
    def get(self, task_id):
        task = find_task(task_id)
        if task is None:
            abort(404, message="Task not found")
        return jsonify(task)
    
    def put(self, task_id):
        task = find_task(task_id)
        if task is None:
            abort(404, message="Task not found")
        
        data = request.get_json()
        validate_task_data(data)
        task["title"] = data.get("title", task["title"])
        task["done"] = data.get("done", task["done"])
        return jsonify(task)
    
    def delete(self, task_id):
        global tasks
        task = find_task(task_id)
        if task is None:
            abort(404, message="Task not found")
        tasks = [task for task in tasks if task["id"] != task_id]
        return {"message": "Task deleted"}, 200
    

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hola, mundo!'}

api.add_resource(HelloWorld, '/')
api.add_resource(TaskList, "/tasks")
api.add_resource(Task, "/tasks/<int:task_id>")

if __name__ == "__main__":
    app.run(debug=True)
