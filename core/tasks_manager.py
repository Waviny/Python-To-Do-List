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

loaded_data = load_tasks()

def menu():
    while True:
        print("1 - ADD TASK\n" \
        "2 - REMOVE TASK\n" \
        "3 - EDIT TASK\n" \
        "4- LEAVE")

        choice = int(input("Enter you're choice : "))

        if choice == 1:
            add_tasks(loaded_data)
            save_tasks(loaded_data)
        elif choice == 2:
            remove_task(loaded_data)
            save_tasks(loaded_data)
        elif choice == 3:
            edit_task(loaded_data)
            save_tasks(loaded_data)
        elif choice == 4:
            break

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
    for i in tasks_data:
        print(tasks_data[i])
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

def edit_task(tasks_data):
    load_tasks()
    existings_id = tasks_data["id"]
    valid_choice = ["tasks", "projects", "data", "priority"]
    for i in tasks_data:
        print(tasks_data[i])
    choice = int(input("Select ID to REMOVE the task : "))
    if choice in existings_id:
        position = tasks_data["id"].index(choice)
        edit_choice = input("What do you want to edit : ")
        if edit_choice in valid_choice:
            change_choice = input("What is the new values : ")
            tasks_data[edit_choice][position] = change_choice
            save_tasks(tasks_data)
        else:
            print("Invalid fields choice ! ")
    else:
        print("Inval input choice ! ")
        edit_task(tasks_data)

def save_tasks(tasks_data):
    any_tasks = json.dumps(tasks_data)
    files = open("data/tasks.json", "w")
    files.write(any_tasks)
    print("Tasks saved successfully")
    files.close()

def main():
    menu()
    


if __name__ == "__main__":
    main()