import os
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)

TASKS_DIR = os.path.join(Path.home(), ".todo")
TASKS_FILEPATH =  os.path.join(TASKS_DIR, "tasks.json")


def get_tasks():
    if os.path.exists(TASKS_FILEPATH):
        with open(TASKS_FILEPATH, "r") as f:
            return json.load(f)
    return {}

def add_task(content):
    tasks = get_tasks()
    if content in tasks:
        logging.error("Une tâche avec le même nom existe déjà.")
        return False

    tasks[content] = False
    _write_tasks_to_file(tasks=tasks)
    return True

def remove_task(content):
    tasks = get_tasks()
    if content not in tasks:
        logging.error("La tâche n'existe pas dans la liste.")
        return False

    del tasks[content]
    _write_tasks_to_file(tasks=tasks)
    return True

def set_task_status(content, done=True):
    tasks = get_tasks()
    if content not in tasks:
        logging.error(f"Aucune tâche trouvée ({content})")
        return False

    tasks[content] = done
    _write_tasks_to_file(tasks=tasks)
    return True

def _write_tasks_to_file(tasks):
    if not os.path.exists(TASKS_DIR):
        os.makedirs(TASKS_DIR)

    with open(TASKS_FILEPATH, "w") as f:
        json.dump(tasks, f, indent=4)
        logging.info("Tâches mises à jour.")


if __name__ == "__main__":
    set_task_status("Chercher la valise", True)