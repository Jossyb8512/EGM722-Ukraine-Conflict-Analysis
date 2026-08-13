# EGM722- Ukraine Conflict Analysis
EGM722 Programming for GIS and Remote Sensing assessment project

## Project Overview

This is the EGM722 Programming for GIS and Remote Sensing assessment project. This project uses Python to automate
the retrieval, processing, spatial analysis and visualisation of conflict event data in Ukraine. 
Armed Conflict and Events Data (ACLED) supplies the event data and an Ukraine boundary dataset provides the Ukrainian
Oblasts for the spatial areas. The analysis calculates conflict event counts and event density by Oblast area then
produces maps, charts and CSV files.  

## Study Period

The analysis covers 12 - 18 July 2025 and is a seven-day historical study period. The same study period is used throughout
the project, including the ACLED request and generated analytical outputs. 

## Data Sources

### ACLED Conflict Event Data

ACLED event data is retrieved through the ACLED API for Ukraine and filtered to the study period. The script requires user
credentials at runtime, and these credentials are not stored within the repository.

### Ukraine Oblast Boundaries

geoBoundaries provides the ADM1 boundary dataset which represents the first level administrative areas (Oblast areas).
This is available in several formats, however, a GeoJSON is used and stored locally in the data/boundaries folder.

## Requirements and Environment

The project was developed in a Conda environment called `ukraine-analysis` using Python 3.11. The repository contains an
`environment.yml` file so that the required environment and packages can be recreated. The `environment.yml` contains the full
dependency list. 
An ACLED account with API access is required because the script asks for credentials when it runs. 
The user will also need Anaconda or Miniconda to create the supplied environment. 

## Installation

Follow these five steps for installation:

1. Clone or download the GitHub repository.
2. Open Anaconda Prompt or another terminal.
3. Navigate to the repository folder.
4. Create the Conda environment from the supplied `environment.yml` file using `conda env create -f environment.yml`.
5. Activate the `ukraine-analysis` environment using `conda activate ukraine-analysis`.

## Running the Analysis

Follow these two steps to run the script: 

1) Run the script from the repository root using `python ukraine_conflict_analysis.py` 
(ensuring the `ukraine-analysis` environment is activated).
2) When prompted enter ACLED email and password.

The script will then retrieve the Ukraine event data for the defined study period, perform the spatial analysis,
and create the outputs automatically.
The script will also print useful status information such as the authentication status, event request status,
total number of events, number of Oblast areas, and the areas with the highest event density.

## Outputs

The script outputs four products:

1. A map, in PNG file format, showing conflict event density by Oblast for Ukraine.
2. A chart, in PNG file format, showing the Top 10 Oblast areas by conflict event count.
3. A chart, in PNG file format, showing conflict events by event type.
4. A summary, in CSV file format, containing:
   1. Oblast name.
   2. Event count.
   3. Area in km².
   4. Events per 1,000 km².

The exact filenames produced are:

1. `ukraine_event_density_12_18_july_2025.png`
2. `top_10_oblast_event_counts_12_18_july_2025.png`
3. `event_types_12_18_july_2025.png`
4. `oblast_area_event_summary_12_18_july_2025.csv`

The filenames include the study period label, which is derived from constants at the top of the script.  

## Repository Structure

```text
EGM722-Ukraine-Conflict-Analysis/
├── data/
│   └── boundaries/
├── docs/
├── outputs/
├── .gitattributes
├── .gitignore
├── environment.yml
├── LICENSE
├── README.md
└── ukraine_conflict_analysis.py
```

`data/boundaries/` contains the input boundary data.
`docs/` contains the project documentation.
`outputs/` stores the generated maps, charts and CSV files.
`environment.yml` defines the Conda environment.
`LICENSE` contains the repository licence.
`README.md` contains the installation and usage information.
`ukraine_conflict_analysis.py` is the main analysis script.

## Data Access and Credentials

 An ACLED account with API access is required, and the script asks for the user's ACLED email and password when it runs.
 `getpass` is used for the password so it is not displayed while typing. For security, credentials are not hard coded
 into the script or stored in the repository. ACLED account permissions affect which event dates are available from the
 API. For the ACLED account used in this project, only historical events with a 12-month delay are available to
 retrieve from the API. geoBoundaries is freely available to download.

## License