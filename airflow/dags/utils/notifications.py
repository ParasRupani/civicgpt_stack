def notify_failure(context):
    dag_id = context.get("dag").dag_id
    task_id = context.get("task_instance").task_id
    execution_date = context.get("execution_date")
    exception = context.get("exception")

    print(f"[ALERT] DAG: {dag_id} | Task: {task_id} failed on {execution_date}")
    print(f"Exception: {exception}")
