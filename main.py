import os
import json
from core import tasks_manager

# Verify Directory & Files
file_path = {
    "assets" : False,
    "core": False,
    "data": False,
    "data/tasks.json": False,
    "logs": False,
    "ui": False,
    "utils": False,
    "core/tasks_manager.py": False 
}

data = {"id": [], "tasks": [], "projects": [], "date": [], "priority": []}
json_string = json.dumps(data)

def dir_verify():
    missing = False
    missing_items = []
    for i in file_path:

        if os.path.exists(i):
            file_path[i] = True
            
        else:

            if i.endswith((".json", ".txt")):
                files = open(i, "w")
                files.write(json_string)
                files.close()

                if os.path.exists(i):
                    file_path[i] = True
                    missing_items.append(i)

                else:
                    print(f"Error : {i} can't created")

            elif i.endswith((".py")):
                files = open(i, "w")
                files.close()

            else:
                os.mkdir(i)

                if os.path.exists(i):
                    file_path[i] = True
                    missing_items.append(i)

                else:
                    print(f"Error {i} can't created")
            missing = True

    if missing == True:
        print("Any directory is missing :", missing_items, "\n" \
        "Creation of missing directory...")
        print("Everything is created")

    else:
        print("All directory are good, the program will be starting")
        return True

def tasks_verify():

    try:
        files = open("data/tasks.json", "r")
        tasks_data = json.load(files)
        print(tasks_data)

    except:
        files = open("data/tasks.json", "w")
        files.write(json_string)
        print("JSON Files are loaded")
        files.close()


def main():

    if dir_verify() == True:
        tasks_verify()


if __name__ == "__main__":
    main()
