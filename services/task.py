user_task = {}

def add_task(user_id, task):
    if user_id not  in user_task:
        user_task[user_id] = []
    user_task[user_id].append(task)

def get_tasks(user_id):
    return user_task.get(user_id, [])