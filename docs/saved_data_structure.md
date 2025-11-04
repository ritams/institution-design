# Saved Data Structure

This document describes the structure of the data saved by the simulation.

## Files

Each simulation run creates a unique directory under `results/`, e.g., `results/run_20251104_155337/`, containing:

- `simulation_data.pkl`: Binary file containing all simulation data.
- `simulation_metadata.yaml`: Human-readable metadata in YAML format.

## Loading the Data

To load the data in Python:

```python
import pickle
import yaml

# Load data
with open('results/run_20251104_155337/simulation_data.pkl', 'rb') as f:
    data = pickle.load(f)

# Load metadata
with open('results/run_20251104_155337/simulation_metadata.yaml', 'r') as f:
    metadata = yaml.safe_load(f)
```

## Data Structure

### `simulation_data.pkl` (Pickle Dict)

The pickle file contains a nested dictionary with the following structure:

```python
{
    theta: {
        ensemble_index: {
            'strategies': [
                [agent0_history],  # List of strategies over time for agent 0
                [agent1_history],  # List of strategies over time for agent 1
                ...
            ],
            'payoffs': [
                [agent0_payoff_history],  # List of payoffs over time for agent 0
                [agent1_payoff_history],  # List of payoffs over time for agent 1
                ...
            ]
        },
        ...
    },
    ...
}
```

- **theta**: Key for each theta value in `theta_list` (e.g., 0, 4, 8, 12, 16).
- **ensemble_index**: Integer from 0 to `ensemble_size - 1` for each ensemble run.
- **strategies**: List of lists, where each sublist is the strategy history (e.g., ['T', 'I', ...]) for one agent over the simulation steps.
- **payoffs**: List of lists, where each sublist is the payoff history (floats) for one agent over the simulation steps.

### `simulation_metadata.yaml` (YAML Dict)

The YAML file contains metadata:

```yaml
N: 1000  # Population size
f_cultural: 0.5  # Fraction of cultural agents
theta_list: [0, 4, 8, 12, 16]  # List of theta values
beta: 0.01  # Learning rate or parameter
max_steps: 50  # Maximum steps per game
ensemble_size: 10  # Number of ensemble runs per theta
equilibria:  # Averaged final fractions per theta
  0: {T: 0.9154, I: 0.0846}
  4: {T: 0.9076, I: 0.0924}
  ...
timestamp: '20251104_155337'  # Run timestamp
run_dir: 'results/run_20251104_155337'  # Directory path
```

- Use this to understand simulation parameters and results summary.
