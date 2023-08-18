# tekton-overhead-measurements

This tool requires a running kubernetes cluster and python 3 installed.

## Install
1. Clone
```
git clone git@github.com:chitrangpatel/tekton-overhead-measurements.git
cd tekton-overhead-measurements
```

2. Install
```
pip install .
```

## Check that everything works
```
python3 execute_and_wait_for_completion.py # this should produce a basic_pod_overhead_times.yaml file
python3 plot_overhead.py # This should produce a basic_pod_overhead_times.png file which you can inspect
```
