from flask import Blueprint, request, jsonify, render_template, current_app
from . import db
from datetime import datetime

main = Blueprint("main", __name__)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    current_app.logger.info("Fetched all tasks")
    return jsonify([{"id": t.id, "title": t.title, "created_at": t.created_at} for t in tasks])

@main.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    if not title:
        current_app.logger.warning("POST /tasks: No title provided")
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    current_app.logger.info(f"Created task: {task.title} (ID: {task.id})")
    return jsonify({"message": "Task created", "id": task.id}), 201

@main.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        current_app.logger.warning(f"DELETE /tasks/{task_id}: Task not found")
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    current_app.logger.info(f"Deleted task ID: {task_id}")
    return jsonify({"message": "Task deleted"})
