# European Temperature Trend Analysis

## Project Overview

This project aims to analyze climate data from Europe to identify trends in temperature changes over recent decades. The analysis utilizes the European Climate Assessment & Dataset (ECA&D) and is implemented using AWS EMR, Apache Spark, and Python.

## Objectives

- Select 5 regions with the most significant temperature changes.
- Create visualizations showing temperature changes over time.
- Publish the source code and report on GitHub.
- Document the project in this README.md file.

## Data Source

European Climate Assessment & Dataset (ECA&D)
[https://www.ecad.eu/](https://www.ecad.eu/)

## Technologies Used

- AWS EMR
- Apache Spark
- Python

## Project Requirements

1. **Selection of Regions**:
   - Identify 5 regions in Europe with the largest temperature changes.

2. **Visualization**:
   - Create visualizations to depict temperature changes over time.

3. **Publication**:
   - Publish the source code and project report on GitHub.

4. **Documentation**:
   - Write the project report and save it in the README.md file.

## Getting Started

### download.py
This Python script is designed to fetch, extract, and format weather data from ECA&D. 
The data is fetched in the form of a zip file, extracted, and then formatted into csv format. 

**File structure**: The script creates directories for the original data and the formatted CSV data. 
The original data is stored in the `./original_data` directory, and the formatted CSV data is stored in the `./csv_data` directory.
Each type of temperature data has its own folder ("mean", "min", "max"). 
The resulting csv temperature data is saved **without** the leading string and zeroes.
This means every type has the same name corresponding to the station source identifier.


**Station Data**: The script also creates a CSV file for station locations from a specified text file. 
The source file is located in the `./original_data/mean` directory and is named `stations.txt`. 
The script skips the header of this file and saves the data as `stations.csv` in the current directory.

The resulting CSV files have the following fields:

| Field | Description                                               |
| ----- |-----------------------------------------------------------|
| STAID | Station identifier                                        |
| SOUID | Source identifier                                         |
| DATE  | Date in "YYYYMMDD" format                                 |
| TN    | Minimum temperature in 0.1 °C                             |
| Q_TN  | Quality code for TN (0='valid'; 1='suspect'; 9='missing') |

This example is for minimum temperature "TN". Max temperature is saved with "TX" and mean with "TG".

### clean_climate_data.py
This Python script is designed to clean and format weather data using PySpark. The script removes invalid data entries, fills missing values with the average temperature, and renames the cleaned CSV files sequentially. It handles three types of temperature data: minimum, mean, and maximum temperatures.

**File structure**: The script processes data stored in the ./csv_data directory and saves the cleaned data in the ./cleaned_data directory. Each type of temperature data has its own folder within both directories ("min", "mean", "max").


**Data Cleaning**: The script performs several cleaning tasks:
- Fills missing/invalid temperature values with the average temperature for that dataset.
- Converts the temperature values from tenths of a degree to degrees Celsius.
- Casts data types to ensure consistency.
- Removes any .crc files and renames the remaining .csv files sequentially.

**Running on EMR**
Ensure PySpark is installed on your EMR cluster. Upload the script to the EMR cluster. SSH into the EMR cluster and run the script:

```poetry run python clean.py```
