# Q1
# Task: Write a Python function using the Flask framework to manage a simple to-do list. Your API should support the 
# following operations: adding a new task, getting a list of all tasks, updating a task description, and deleting a task.

# Input Format: For adding a new task, the input should be a JSON object like `{“task”: “Buy groceries”}`.

# Constraints:

# The task description will be a non-empty string.
# Each task will have a unique identifier.
# Output Format: The output should also be in JSON format. For fetching all tasks, the output should look like
# `[{“id”: 1, “task”: “Buy groceries”}, {“id”: 2, “task”: “Read a book”}]`.


from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []

task_id = 1

@app.route('/tasks', methods=['GET'])

def get_tasks():

    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])

def add_task():

    global task_id

    new_task = {"id": task_id, "task": request.json['task']}

    tasks.append(new_task)

    task_id += 1

    return jsonify(new_task), 201

@app.route('/tasks/<int:id>', methods=['PUT'])

def update_task(id):

    task = next((item for item in tasks if item['id'] == id), None)

    if task is None:

        return jsonify({"error": "Task not found"}), 404

    task['task'] = request.json['task']

    return jsonify(task)

@app.route('/tasks/<int:id>', methods=['DELETE'])

def delete_task(id):

    global tasks

    tasks = [task for task in tasks if task['id'] != id]

    return jsonify({"result": "Task deleted"})