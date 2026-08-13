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

## Installation

## Running the Analysis

## Outputs

## Repository Structure

## Data Access and Credentials

## License