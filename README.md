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
| ----- | --------------------------------------------------------- |
| STAID | Station identifier                                        |
| SOUID | Source identifier                                         |
| DATE  | Date in "YYYYMMDD" format                                 |
| TN    | Minimum temperature in 0.1 °C                             |
| Q_TN  | Quality code for TN (0='valid'; 1='suspect'; 9='missing') |

This example is for minimum temperature "TN". Max temperature is saved with "TX" and mean with "TG".

**Running the script**:

1. Make sure your dependencies are up to date using `poetry update`
2. `poetry run python src/download.py`

### clean.py

This Python script is designed to clean and format weather data using PySpark. The script removes invalid data entries, fills missing values with the average temperature, and renames the cleaned CSV files sequentially. It handles three types of temperature data: minimum, mean, and maximum temperatures.

**File structure**: The script processes data stored in the ./csv_data directory and saves the cleaned data in the ./cleaned_data directory. Each type of temperature data has its own folder within both directories ("min", "mean", "max").

**Data Cleaning**: The script performs several cleaning tasks:

- Fills missing/invalid temperature values with the average temperature for that dataset.
- Converts the temperature values from tenths of a degree to degrees Celsius.
- Casts data types to ensure consistency.
- Removes any .crc files and renames the remaining .csv files sequentially.

**Running the script**:

1. Make sure you have downloaded the data using `download.py`
2. Make sure your dependencies are up to date using `poetry update`
3. `poetry run python src/clean.py`

### yearly_query.py

This python script is designed to prepare data format for plot visualization. It splits data by station ID and calculates an average temperature for each year for every station. It handles evaluation of min/max/mean yearly temperature separately.

**File structure**
The script processes data stored in ./cleaned_data and saves the results of specific stations in the ./yearly_data directory. Similarly to cleaned_data, the division into ("min", "mean", "max") subfolders has been maintained to facilitate visualization. In the appropiate subfolders there are further subfolders named STAID="station_identifier"", which contain a csv file with information for each year for the selected station.

- **Destination Directory: `yearly_data`**

  - `min/`
    - `STAID=A/`
      - `<generated_csv_file_name>.csv` (for min, station A)
    - `STAID=B/`
      - `<generated_csv_file_name>.csv` (for min, station B)
  - `max/`
    - `STAID=C/`
      - `<generated_csv_file_name>.csv` (for max, station C)
    - `STAID=D/`
      - `<generated_csv_file_name>.csv` (for max, station D)
  - `mean/`
    - `STAID=E/`
      - `<generated_csv_file_name>.csv` (for mean, station E)
    - `STAID=F/`
      - `<generated_csv_file_name>.csv` (for mean, station F)

**Calculating the average annual temperature**
The script appropriately analyzes subsequent csv files, for each found ID and for each year of data collected by the station, it calculates the average temperature and the result is added to the csv file created for a given station.

**Running the script**:

1. Make sure you have downloaded the data using `download.py` and cleaned them using `clean.py`
2. Make sure your dependencies are up to date using `poetry update`
3. `poetry run python src/yearly_query.py`

### detect_top5_temperature_changes.py

**Detect 5 Areas with the Biggest Temperature Changes**:

Detect 5 Areas with the Biggest Temperature Changes of all time for each station with a quality code for TN = 0 (0 - 'valid', 1 - 'suspect, 9 - 'missing')

1. Make sure you have downloaded the data using `download.py`
2. Make sure your dependencies are up to date using `poetry update`
3. Make sure you have cleaned the data with `clean.py`
4. ```poetry run python src/detect_top5_temperature_changes.py```

## Steps in the ETL process

1. `download.py`
2. `clean.py`
3. `detect_top5_temperature_changes.py`

## Climate Data Column Descriptions

This document provides detailed information about each column in the climate dataset used for the European Temperature Trend Analysis project. It includes the data type, description, possible values, and relevance of each column.

### Columns in the Temperature Data CSV Files

| Column Name | Data Type | Description | Possible Values | Relevance |
| ----------- | --------- | ----------- | --------------- | --------- |
| `STAID`     | Integer   | Station identifier, a unique ID for each weather station. | Any positive integer (e.g., 12345) | Highly relevant. Used to identify the source of the temperature data. |
| `SOUID`     | Integer   | Source identifier, another unique ID related to the data source. | Any positive integer (e.g., 67890) | Less relevant. Helps in cross-referencing the data source. |
| `DATE`      | String    | Date of the temperature measurement in "YYYYMMDD" format. | Any valid date string (e.g., "20240101") | Highly relevant. Used for time-series analysis of temperature changes. |
| `TN`        | Float     | Minimum temperature of the day in tenths of degrees Celsius. | Any float value (e.g., -120.0 to 450.0, representing -12.0°C to 45.0°C) | Highly relevant. Represents daily minimum temperatures, essential for trend analysis. |
| `Q_TN`      | Integer   | Quality code for `TN`. Indicates the reliability of the data. | 0 (valid), 1 (suspect), 9 (missing) | Relevant. Helps in data cleaning by identifying and handling invalid or missing data. |
| `TX`        | Float     | Maximum temperature of the day in tenths of degrees Celsius. | Any float value (e.g., -120.0 to 450.0, representing -12.0°C to 45.0°C) | Highly relevant. Represents daily maximum temperatures, essential for trend analysis. |
| `Q_TX`      | Integer   | Quality code for `TX`. Indicates the reliability of the data. | 0 (valid), 1 (suspect), 9 (missing) | Relevant. Helps in data cleaning by identifying and handling invalid or missing data. |
| `TG`        | Float     | Mean temperature of the day in tenths of degrees Celsius. | Any float value (e.g., -120.0 to 450.0, representing -12.0°C to 45.0°C) | Highly relevant. Represents daily mean temperatures, essential for trend analysis. |
| `Q_TG`      | Integer   | Quality code for `TG`. Indicates the reliability of the data. | 0 (valid), 1 (suspect), 9 (missing) | Relevant. Helps in data cleaning by identifying and handling invalid or missing data. |

### Columns in the Station Data CSV File

| Column Name | Data Type | Description | Possible Values | Relevance |
| ----------- | --------- | ----------- | --------------- | --------- |
| `STAID`     | Integer   | Station identifier, a unique ID for each weather station. | Any positive integer (e.g., 12345) | Highly relevant. Used to identify the source of the temperature data. |
| `STANAME`   | String    | Name of the weather station. | Any string (e.g., "Amsterdam") | Less relevant. Can be useful for understanding the geographical context. |
| `CN`        | String    | Country code where the station is located. | Any two-letter country code (e.g., "NL" for Netherlands) | Relevant. Helps in regional analysis and filtering data by country. |
| `LAT`       | Float     | Latitude of the weather station. | Any float value (e.g., 52.3676) | Highly relevant. Useful for mapping and spatial analysis. |
| `LON`       | Float     | Longitude of the weather station. | Any float value (e.g., 4.9041) | Highly relevant. Useful for mapping and spatial analysis. |
| `HGHT`      | Float     | Height above sea level of the weather station. | Any float value (e.g., 12.0) | Slightly elevant. Can be useful for understanding climate patterns related to altitude. |
| `START`     | Integer   | Year when the station started recording data. | Any year (e.g., 1950) | Relevant. Helps in understanding the historical range of data availability. |
| `STOP`      | Integer   | Year when the station stopped recording data (if applicable). | Any year or null if still active (e.g., 2020 or null) | Relevant. Useful for filtering and understanding data continuity. |
| `SOURCE`    | String    | Source of the data. | Any string (e.g., "ECA&D") | Less relevant. Useful only for data provenance and quality assessment. |

## Docs

---

### How to run

#### Docker

1. **Install Docker**: Ensure that Docker is installed and running on your computer. You can download it from the [official Docker website](https://www.docker.com/get-started).
2. **Run the Documentation Server**:
   Use the following command to start the documentation server with Docker. This command mounts your current directory to the `/docs` directory in the container and starts the MkDocs server with the Material theme.

    ```bash
    docker run --rm -it -v ${PWD}:/docs squidfunk/mkdocs-material new .
    ```

Note: If you are using a Windows command prompt, replace `${PWD}` with `%cd%`. If you're using PowerShell, use `${PWD}`.

#### Python

1. **Install Python**: Ensure that Python is installed on your computer. You can download it from the [official Python website](https://www.python.org/downloads/). It's recommended to use Python 3.6 or higher.

2. **Install Project Dependencies**:
Navigate to the project directory and install the required dependencies using the following command:

    ```bash
    python -m pip install -r requirements.txt
    ```

3. **Run the Documentation Server**:
Start the local MkDocs server using the command below. This will serve your documentation site locally and enable live reloading for changes.

    ```bash
    python -m mkdocs serve
    ```

After running this command, you should see output indicating that the server is running, and you can view your documentation in a web browser at the address provided (typically `http://127.0.0.1:8000/`).

#### Summary

Each column in the climate dataset has a specific role in the overall analysis. The temperature columns (`TN`, `TX`, `TG`) are crucial for identifying trends in minimum, maximum, and mean temperatures. The quality codes (`Q_TN`, `Q_TX`, `Q_TG`) help ensure data integrity by marking suspect or missing data points. The station-related columns (`STAID`, `STANAME`, `CN`, `LAT`, `LON`, `HGHT`, `START`, `STOP`, `SOURCE`) provide essential metadata for spatial and temporal analysis, enabling a deeper understanding of the geographical and historical context of the temperature data.

---
