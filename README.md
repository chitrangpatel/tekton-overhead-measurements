# tekton-overhead-measurements

This tool requires a running kubernetes cluster and python 3 installed.

## Install
1. Clone
```bash
git clone https://github.com/chitrangpatel/tekton-overhead-measurements.git 
cd tekton-overhead-measurements
```

2. Install
```bash
pip install -r requirements.txt
```

## Check that everything works
```bash
python3 execute_and_wait_for_completion.py # this should produce a basic_pod_overhead_times.yaml file
python3 plot_overhead.py # This should produce a basic_pod_overhead_times.png file which you can inspect
```
