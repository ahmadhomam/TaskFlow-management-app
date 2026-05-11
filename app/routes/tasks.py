from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db, socketio
from app.models import Task
from app.analytics import get_analytics

tasks_bp = Blueprint("tasks", __name__)

# Basic validation sets
PRIORITIES = {"low", "medium", "high"}
STATUSES = {"pending", "in_progress", "completed"}

def broadcast_change(action, task_data):
    """Helper to push socket updates to the frontend"""
    socketio.emit("task_update", {"action": action, "task": task_data})

@tasks_bp.route("/", methods=["GET"])
@login_required
def get_tasks():
    # Base query for user's tasks
    query = Task.query.filter_by(user_id=current_user.id)

    # Optional filtering
    status = request.args.get("status")
    priority = request.args.get("priority")

    if status in STATUSES:
        query = query.filter_by(status=status)
    if priority in PRIORITIES:
        query = query.filter_by(priority=priority)

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify({"tasks": [t.to_dict() for t in tasks]})

@tasks_bp.route("/", methods=["POST"])
@login_required
def add_task():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    # Validate priority if provided
    priority = data.get("priority", "medium").lower()
    if priority not in PRIORITIES:
        return jsonify({"error": "Invalid priority level"}), 400

    new_task = Task(
        title=data["title"].strip(),
        description=data.get("description", "").strip(),
        priority=priority,
        status="pending",
        user_id=current_user.id
    )
    
    db.session.add(new_task)
    db.session.commit()

    broadcast_change("created", new_task.to_dict())
    return jsonify({"message": "Task added", "task": new_task.to_dict()}), 201

@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}

    # Update fields if they exist in request
    if "title" in data:
        task.title = data["title"].strip()
    if "description" in data:
        task.description = data["description"].strip()
    
    if "priority" in data:
        if data["priority"] in PRIORITIES:
            task.priority = data["priority"]
            
    if "status" in data:
        if data["status"] in STATUSES:
            task.status = data["status"]

    db.session.commit()
    broadcast_change("updated", task.to_dict())
    
    return jsonify({"message": "Task updated", "task": task.to_dict()})

@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    task_data = task.to_dict()
    db.session.delete(task)
    db.session.commit()

    broadcast_change("deleted", task_data)
    return jsonify({"message": "Task deleted"})

@tasks_bp.route("/analytics", methods=["GET"])
@login_required
def run_analytics():
    # Pass user tasks to the pandas helper
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    stats = get_analytics([t.to_dict() for t in tasks])
    return jsonify(stats)