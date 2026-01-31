# Integrated Methodology for Assessing Item Discrimination
[![DOI](https://zenodo.org/badge/815342545.svg)](https://doi.org/10.5281/zenodo.14782717)

To use this methodology, do the following: 

1. Place data in "data" folder.

2. Run the following scripts in order:
    - `run_analyses.py`: Main script to run analyses and generate results.
    - `generate_plots.py`: Generates all figures and plots, including heatmaps and distractor analysis.
    - `export_plot_data.py`: Exports data used for plotting.

## Directory Structure
```
.
├── analyses/                  # Core analysis logic and modules
├── data/                      # Input data directory
├── figures/                   # Generated plots and figures
├── results/                   # Analysis outputs and dataframes
├── environment/               # Environment configuration
├── run_analyses.py           # Main script to run analyses
├── generate_plots.py         # Script to generate all figures
├── export_plot_data.py       # Script to export data for plotting
└── README.md                 # Project documentation
```
This repository is the companion for paper "Towards an Integrated Methodology for Assessing Item Discrimination."

It is maintained by Russell Jeter: <https://sites.gsu.edu/rjeter>. If you have any concerns, please submit a Github issue, or email me at [rjeter@gsu.edu](mailto:rjeter@gsu.edu).
