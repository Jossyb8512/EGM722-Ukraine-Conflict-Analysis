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

## Outputs

## Repository Structure

## Data Access and Credentials

## License