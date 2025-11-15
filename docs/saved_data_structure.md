# Saved Data Structure

This document describes the structure of the data saved by the simulation.

## Files

Each simulation run creates a unique pickle file under `results/data` directory.

- `<fname>.pkl`: Binary file containing all simulation data.
- `<fname>.pkl` is generated using the `get_fname` function defined in `src/utils.py`.
- `<fname>.pkl` follows the format: `data_N_{N}_f_cultural_{f_cultural}_theta_list_{theta_list}_beta_{beta:.3f}_max_steps_{max_steps}_ensemble_size_{ensemble_size}_update_fraction_{update_fraction:.3f}.pkl`


## Loading the Data

To load the data in Python:

```python
import pickle

# Load data
with open('results/data/data_N_1000_f_cultural_0.75_theta_list_15_1_13_beta_0.100_max_steps_50_ensemble_size_100_update_fraction_0.100.pkl', 'rb') as f:
    data = pickle.load(f)

```
or use the `load_data` function defined in the `notebooks/analysis.ipynb`

## Data Structure

### `<fname>.pkl` (Pickle Dict)

The pickle file contains a nested dictionary with the following structure:

```python
{
    game_index: {
        ensemble_index: {
            'strategies': [
                [agent0_history],  # List of strategies over time for agent 0
                [agent1_history],  # List of strategies over time for agent 1
                ...
            ],
            'theta': theta_value,
        },
        ...
    },
    ...
}
```

- **game_index**: Integer from 0 to `len(theta_list) - 1` for each theta value in `theta_list` (e.g., 0, 4, 8, 12, 16).
- **ensemble_index**: Integer from 0 to `ensemble_size - 1` for each ensemble run.
- **strategies**: List of lists, where each sublist is the strategy history (e.g., ['T', 'I', ...]) for one agent over the simulation steps.
- **theta**: The theta value for the current game.


