import time
import json
import os
json_file = "tasks.json"
task_command = ["update", "delete", "mark-in-progress", "mark-done", "add", "list", "quit"]
tasks = {}     

class Task:
    def __init__(self, id, description, status, created_at, updated_at):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def update(self, input):
        self.description = input
        self.updated_at = time.ctime()

    
    def mark_done(self):
        self.status = "done"
    
    def mark_in_progress(self):
        self.status = "in progress"
        
if os.stat(json_file).st_size != 0: # If the json file is not empty, the information is collected
    with open(json_file, "r") as file:
        tasks_raw = json.load(file)
    for i in tasks_raw:
        task = Task(i["id"], i["description"], i["status"], i["created_at"], i["updated_at"])
        tasks.update({task.id: task})
        

    
def add(command):
    command.pop(0) #isolates the description
    print("made it to add")
    task = Task((len(tasks)+1), " ".join(command), "not done", time.ctime(), None)
    tasks[task.id] = task
    
def delete(command):
    if len(command) > 2 or not command[1].isdigit(): # further ensure the correctness of the command
        print("That is not a valid command")
    else:
        del tasks[int(command[1])] # deletes task, casting to string to an int and using as the index
        for key, value in tasks.items(): # moves everything in the list to fill in the gap made
            if key > int(command[1]): 
                new_key = key - 1
                key = new_key
                new_id = value.id - 1
                value.id = new_id
                
def update(command):
    if not command[1].isdigit():
        print("invalid command")
    desired_key = command[1]
    command.pop(1)
    command.pop(0)
    for key, value in tasks.items():
        if int(desired_key) == key:
            new_description = " ".join(command)
            value.update(new_description)
            

def mark_complete(command):
    if len(command) > 2 or len(command) < 2 or not command[1].isdigit():
        print("invalid command")
    else:
         for key, value in tasks.items():
             if key == int(command[1]):
                 value.mark_done()
                 
def in_progress(command):
    if len(command) > 2 or len(command) < 2 or not command[1].isdigit():
        print("invalid command")
    else:
         for key, value in tasks.items():
             if key == int(command[1]):
                 value.mark_in_progress()
            
                
        
def list_items():
    print("made it to list items")
    for value in tasks:
        print(tasks[value].__dict__)

    
while True:
    user_input = input()
    command = user_input.split()
    if len(command) == 0 or command[0] not in task_command:
        print("That is not a valid command")
        continue
    if command[0] == "add":
        add(command)
    elif command[0] == "list":
        list_items()
    elif command[0] == "delete":
        delete(command)
    elif command[0] == "update":
        update(command)
    elif command[0] == "mark-done":
        mark_complete(command)
    elif command[0] == "mark-in-progress":
        in_progress(command)
    elif command[0] == "quit":
        print("quiting")
        break
    else:
        print("not a valid command") # because everything is supposed to be a command, 
                                     # nothing is converted to lower case
    


task_dict = []
with open("tasks.json", "w") as file:
    for task in tasks:
        task_dict.append(tasks[task].__dict__)
    json.dump(task_dict, file, indent=4)



