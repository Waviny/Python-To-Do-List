import json
import os

# --- Données par défaut ---
DATA_FILE = "data/tasks.json"
DEFAULT_DATA = {"id": [], "tasks": [], "projects": [], "date": [], "priority": [], "status": []}


# --- Chargement des tâches ---
def load_tasks():
    """Charge les tâches depuis le fichier JSON ou crée le fichier s'il n'existe pas."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, indent=4)
        print("✅ Nouveau fichier tasks.json créé.")
        return DEFAULT_DATA

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            print("⚠️ Fichier JSON corrompu. Réinitialisation...")
            save_tasks(DEFAULT_DATA)
            return DEFAULT_DATA


# --- Sauvegarde des tâches ---
def save_tasks(data):
    """Sauvegarde les tâches dans le fichier JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# --- Ajouter une tâche ---
def add_task(task_data):
    """Ajoute une tâche au fichier JSON."""
    data = load_tasks()
    new_id = data["id"][-1] + 1 if data["id"] else 1

    data["id"].append(new_id)
    data["tasks"].append(task_data["task"])
    data["projects"].append(task_data["project"])
    data["date"].append(task_data["date"])
    data["priority"].append(task_data["priority"])
    data["status"].append(task_data["status"])

    save_tasks(data)
    return new_id


# --- Supprimer une tâche ---
def remove_task(task_id):
    """Supprime une tâche par ID."""
    data = load_tasks()

    if task_id in data["id"]:
        idx = data["id"].index(task_id)
        for key in data.keys():
            data[key].pop(idx)
        save_tasks(data)
        return True
    else:
        print(f"Tâche {task_id} introuvable.")
        return False


# --- Modifier une tâche ---
def edit_task(task_id, field, new_value):
    """Modifie un champ spécifique d'une tâche."""
    data = load_tasks()

    valid_fields = ["tasks", "projects", "date", "priority", "status"]
    if field not in valid_fields:
        raise ValueError(f"Champ invalide : {field}")

    if task_id not in data["id"]:
        raise ValueError(f"Tâche ID {task_id} introuvable")

    idx = data["id"].index(task_id)
    data[field][idx] = new_value
    save_tasks(data)
    return True
