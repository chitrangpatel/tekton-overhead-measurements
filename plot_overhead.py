import matplotlib.pyplot as plt
import yaml
import datetime
import sys

def plot_pod_overhead(plt, task_start_times, task_stop_times, step_start_times, offset_x_values, colors, width, label):
    """Makes a bar plot per task to show the overhead."""
    #plt.bar([i+1+offset_x_values for i in range(len(task_stop_times))], [(task_stop_times[i] - task_start_times[i]).total_seconds() for i in range(len(task_stop_times))], color=colors[0], width=width, label=f"execution time: {label}")
    plt.bar([i+1+offset_x_values for i in range(len(step_start_times))], [(step_start_times[i] - task_start_times[i]).total_seconds() for i in range(len(step_start_times))], color =colors[1], width=width, label=f"pod start time: {label}")

def load_measurements(filename):
    f = yaml.safe_load(open(data_path))
    task_stop_times = [datetime.datetime.fromisoformat(t) for t in f['task_stop_times']]
    task_start_times = [datetime.datetime.fromisoformat(t) for t in f['task_start_times']]
    step_start_times = [datetime.datetime.fromisoformat(t) for t in f['step_start_times']]
    return task_stop_times, task_start_times, task_stop_times

def plot(name = "workspace_comparison"):
    plt.figure(figsize=(12, 4))
    
    data_path = f"{name}_times.yaml"
    # plot GKE measurements
    task_stop_times, task_start_times, task_stop_times = load_measurements(data_path) 
    plot_pod_overhead(plt, task_start_times, task_stop_times, step_start_times, -0.15, ['#7efcd2', '#fc7ea8'], 0.3, "GKE")
    
    # plot minikiube measurements
    #task_stop_times, task_start_times, task_stop_times = load_measurements(f'{name}_times_minikube.yaml')
    #plot_pod_overhead(plt, task_start_times, task_stop_times, step_start_times, 0.15, ['orange', '#7efcd2'], 0.3, "Minikube:VM")
    
    plt.ylabel('Time(s)')
    plt.xlabel("TaskRuns")
    plt.legend(loc=(0.85, 0.95))
    plt.xlim(0, len(task_start_times) + 1)
    plt.title(f"Execution of PipelineRun with {len(task_start_times)} TaskRuns")
    plt.xticks([i+1 for i in range(len(task_start_times))])
    plt.savefig(data_path.replace('.yaml', '.png'))

if __name__=="__main__":
    name = sys.argv[1]
    plot(name)
