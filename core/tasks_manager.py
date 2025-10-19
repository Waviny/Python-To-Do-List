import json

data = {"id": [], "tasks": [], "projects": [], "date": [], "priority": []}
json_string = json.dumps(data)
        
def load_tasks():

    try:
        files = open("data/tasks.json", "r")
        tasks_data = json.load(files)
        return tasks_data

    except:
        files = open("data/tasks.json", "w")
        files.write(json_string)
        print("JSON Files are loaded")
        files.close()
        return data

def add_tasks(tasks_data):
    task_name = input("Enter you're task name : ")
    task_project = input("Enter you're task project : ")
    task_date = input("Enter you're task date : ")
    task_priority = input("Enter you're task priority ( 1 - 10 ) : ")

    if len(tasks_data["id"]) == 0:
        index = 0
    else:
        index = tasks_data["id"][-1]

    tasks_data["id"].append(index+1)
    tasks_data["tasks"].append(task_name)
    tasks_data["projects"].append(task_project)
    tasks_data["date"].append(task_date)
    tasks_data["priority"].append(task_priority)
    save_tasks(tasks_data)

def remove_task(tasks_data):
    load_tasks()
    choice = int(input("Select ID to REMOVE the task : "))
    position = tasks_data["id"].index(choice)
    for i in tasks_data["id"]:
        if choice == i:
            tasks_data["id"].pop(position)
            tasks_data["tasks"].pop(position)
            tasks_data["projects"].pop(position)
            tasks_data["date"].pop(position)
            tasks_data["priority"].pop(position)
    save_tasks(tasks_data)  


def save_tasks(tasks_data):
    any_tasks = json.dumps(tasks_data)
    files = open("data/tasks.json", "w")
    files.write(any_tasks)
    print("Tasks saved successfully")
    files.close()

def main():
    loaded_data = load_tasks()
    save_tasks(loaded_data)
    remove_task(loaded_data)
    


if __name__ == "__main__":
    main()