import os
from dateutil import parser
from kubernetes import client, config, watch
import yaml
import sys

config.load_kube_config()

def execute_all_tasks(tasks_path="tasks", namespace="overhead"):
    os.system(f"kubectl delete -R -f {tasks_path}/")
    os.system(f"kubectl apply -R -f {tasks_path}/")

def execute_pipeline(pipeline_path):
    os.system(f"kubectl delete -f {pipeline_path}")
    os.system(f"kubectl apply -f {pipeline_path}")

def read_times_from_tasks(tasks):
    task_start_times = []
    task_stop_times = []
    step_start_times = []
    step_stop_times = []
    for t in tasks:
        t1st = parser.isoparse(t['status']['startTime'])
        task_start_times.append(t1st.isoformat())
        for s in t['status']['steps']:
            sSA = parser.isoparse(s['terminated']['startedAt'])
            step_start_times.append(sSA.isoformat())
            sFA = parser.isoparse(s['terminated']['finishedAt'])
            step_stop_times.append(sFA.isoformat())
        t1ct = parser.isoparse(t['status']['completionTime'])
        task_stop_times.append(t1ct.isoformat())
    payload = {
        "step_start_times": step_start_times,
        "step_stop_times": step_stop_times,
        "task_start_times": task_start_times,
        "task_stop_times": task_stop_times,
    }
    return payload

def wait_until_complete():
    v1 = client.CustomObjectsApi()
    w = watch.Watch()
    status = False
    final_object = None
    for event in w.stream(v1.list_cluster_custom_object, "tekton.dev", "v1", "pipelineruns"):#, _request_timeout=60):
        if 'status' in event['object'] and 'conditions' in event['object']['status']:
            final_object = event['object']
            cond = event['object']['status']['conditions'][0]
            if cond['status'] == "True":
                print(cond)
                w.stop()
                status = True
            elif cond['status'] == "False":
                w.stop()
            else:
                print("Still running: ", cond)
    print("Ended: ", status)
    return status, final_object

def get_child_tasks(pipeline):
    tasks = set()
    for cr in pipeline['status']['childReferences']:
        tasks.add(cr['name'])
    v1 = client.CustomObjectsApi()
    child_tasks = []
    ret = v1.list_cluster_custom_object("tekton.dev", "v1", "taskruns")
    for t in ret['items']:
        if t['metadata']['name'] in tasks:
            child_tasks.append(t)
    return child_tasks 

def main():
    pipeline_name = sys.argv[1]
    output_file = f"{pipeline_name}_times.yaml"
    execute_all_tasks()
    execute_pipeline(f"pipelines/{pipeline_name}.yaml")
    status, pipeline_obj = wait_until_complete()
    if status is True:
        tasks = get_child_tasks(pipeline_obj)
        times = read_times_from_tasks(tasks) 
        yaml.dump(times, open(output_file, 'w'))

if __name__=="__main__":
    main()
