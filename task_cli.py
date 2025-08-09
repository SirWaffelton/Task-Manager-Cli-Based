import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []
    return tasks

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def get_current_timestamp():
    return datetime.now().isoformat(timespec='seconds')

def generate_task_id(tasks):
    if not tasks:
        return 1
    else:
        max_id = max(task["id"] for task in tasks)
        return max_id + 1

def create_task(description, tasks):
    task_id = generate_task_id(tasks)
    timestamp = get_current_timestamp()
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": timestamp,
        "updatedAt": timestamp
    }
    return new_task

def add_task_interactive(tasks):
    description = input("Enter a new task description: ").strip()
    if description:
        new_task = create_task(description, tasks)
        tasks.append(new_task)
        save_tasks(tasks)
        print(f'Task added successfully! (ID: {new_task["id"]})')
    else:
        print("Task description cannot be empty.")


def list_tasks(tasks, status_filter=None):
    filtered_tasks = tasks
    if status_filter:
        filtered_tasks = [t for t in tasks if t["status"] == status_filter]
        
    if not filtered_tasks:
        print("No tasks found.")
        return
    for task in filtered_tasks:
          print(f'ID: {task["id"]} | Description: {task["description"]} | Status: {task["status"]} | Created: {task["createdAt"]} | Updated: {task["updatedAt"]}')

def delete_task(tasks, task_id):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            print(f"Task {task_id} deleted successfully.")
            return
    print(f"Task {task_id} not found.")
        
def update_task_status(tasks, task_id, new_status):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = get_current_timestamp()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}.")
            return
    print(f"Task {task_id} not found.")
    
def main_menu():
    print("\nCommands:")
    print("1 - Add Task")
    print("2 - List All Tasks")
    print("3 - List Done Tasks")
    print("4 - List Todo Tasks")
    print("5 - List In-Progress Tasks")
    print("6 - Delete Task")
    print("7 - Mark Task In-Progress")
    print("8 - Mark Task Done")
    print("9 - Exit")

    while True:
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            description = input("Enter task description: ").strip()
            if description:
                new_task = create_task(description, tasks)
                tasks.append(new_task)
                save_tasks(tasks)
                print(f"Task added with ID {new_task['id']}")
            else:
                print("Task description cannot be empty.")
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            list_tasks(tasks, "done")
        elif choice == "4":
            list_tasks(tasks, "todo")
        elif choice == "5":
            list_tasks(tasks, "in-progress")
        elif choice == "6":
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
                delete_task(tasks, task_id)
            except ValueError:
                print("Invalid task ID.")
        elif choice == "7":
            try:
                task_id = int(input("Enter task ID to mark in-progress: ").strip())
                update_task_status(tasks, task_id, "in-progress")
            except ValueError:
                print("Invalid task ID.")
        elif choice == "8":
            try:
                task_id = int(input("Enter task ID to mark done: ").strip())
                update_task_status(tasks, task_id, "done")
            except ValueError:
                print("Invalid task ID.")
        elif choice == "9":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    tasks = load_tasks()
    print("Loaded tasks:", tasks)
    main_menu()