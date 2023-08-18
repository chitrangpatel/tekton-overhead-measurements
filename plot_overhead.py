import matplotlib.pyplot as plt
import yaml
import datetime

def plot_pod_overhead(plt, task_start_times, task_stop_times, step_start_times, offset_x_values, colors, width, label):
    """Makes a bar plot per task to show the overhead."""
    plt.bar([i+1+offset_x_values for i in range(len(task_stop_times))], [(task_stop_times[i] - task_start_times[i]).total_seconds() for i in range(len(task_stop_times))], color=colors[0], width=width, label=f"execution time: {label}")
    plt.bar([i+1+offset_x_values for i in range(len(step_start_times))], [(step_start_times[i] - task_start_times[i]).total_seconds() for i in range(len(step_start_times))], color =colors[1], width=width, label=f"pod start time: {label}")

def plot(data_path = "basic_pod_overhead_times.yaml"):
    # load GKE measurements
    f = yaml.safe_load(open(data_path))
    task_stop_times = [datetime.datetime.fromisoformat(t) for t in f['task_stop_times']]
    task_start_times = [datetime.datetime.fromisoformat(t) for t in f['task_start_times']]
    step_start_times = [datetime.datetime.fromisoformat(t) for t in f['step_start_times']]
    
    
    # Now plot
    plt.figure(figsize=(12, 4))
    
    plot_pod_overhead(plt, task_start_times, task_stop_times, step_start_times, 0, ['#7efcd2', '#fc7ea8'], 0.3, "GKE")
    ## load minikiube measurements
    #f = yaml.safe_load(open('tekton_on_vms/basic_timing_minikube.yaml'))
    #mini_task_stop_times = f['task_stop_times']
    #mini_task_start_times = f['task_start_times']
    #mini_step_start_times = f['step_start_times']
    #plot_pod_overhead(plt, mini_task_start_times, mini_task_stop_times, mini_step_start_times, 1.15, ['orange', 'black'], 0.3, "Minikube in VM")
    #plt.bar([i+1-0.15 for i in range(len(task_stop_times))], [(task_stop_times[i] - task_start_times[i]).total_seconds() for i in range(len(task_stop_times))], color ='#7efcd2', width = 0.3, label="execution time:GKE")
    #plt.bar([i+1-0.15 for i in range(len(step_start_times))], [(step_start_times[i] - task_start_times[i]).total_seconds() for i in range(len(step_start_times))], color ='#fc7ea8', width = 0.3, label="pod start time:GKE")
    #plt.bar([i+1+0.15 for i in range(len(mini_task_stop_times))], [(mini_task_stop_times[i] - mini_task_start_times[i]).total_seconds() for i in range(len(mini_task_stop_times))], color ='orange', width = 0.3, label="execution time:Minikube in VM")
    #plt.bar([i+1+0.15 for i in range(len(mini_step_start_times))], [(mini_step_start_times[i] - mini_task_start_times[i]).total_seconds() for i in range(len(mini_step_start_times))], color ='black', width = 0.3, label="pod start time:Minikube in VM")
    
    plt.ylabel('Time(s)')
    plt.xlabel("TaskRuns")
    plt.legend(loc=(0.85, 0.8))
    plt.xlim(0, len(task_start_times) + 1)
    #plt.axis('tight')
    plt.title(f"Execution of PipelineRun with {len(task_start_times)} TaskRuns")
    plt.xticks([i+1 for i in range(len(task_start_times))])
    plt.savefig(data_path.replace('.yaml', '.png'))

plot()
