# Project Report: Temperature Analysis Project

---

## Technologies Used

1. **Python**: The primary programming language used for this project.
2. **Libraries**:
   - **Pandas**: For data manipulation and analysis.
   - **Requests**: For making HTTP requests to download data.
   - **Matplotlib**: For plotting and visualizing data.
   - **OS**: For interacting with the operating system to handle file paths.
   - **Numpy**: For numerical operations.
3. **Jupyter Notebook**: For running and testing the Python code.
4. **Markdown**: For creating this comprehensive project report.

---

## Problems Encountered

1. **Data Cleaning**: Handling missing or inconsistent data in the datasets.
2. **HTTP Requests**: Dealing with failed downloads or incomplete data retrieval.
3. **Data Analysis**: Identifying the correct statistical methods to detect significant temperature changes.
4. **Code Integration**: Ensuring that different scripts work seamlessly together.

---

## Detailed Description of the Code

### `download.py`
- **Purpose**: This script is responsible for downloading the temperature data from a specified URL.
- **Key Functions**:
  - `download_data(url, save_path)`: Downloads the data from the given URL and saves it to the specified path.
- **Technologies**: Uses the `requests` library to handle HTTP requests and `os` for file path operations.

### `clean.py`
- **Purpose**: This script cleans the downloaded data, handling missing values and ensuring the data is in a consistent format.
- **Key Functions**:
  - `clean_data(file_path)`: Reads the data from the given file path, cleans it, and returns a cleaned DataFrame.
- **Technologies**: Utilizes `pandas` for data manipulation.

### `yearly_query.py`
- **Purpose**: This script queries the cleaned data to provide yearly statistics and trends.
- **Key Functions**:
  - `query_yearly_data(cleaned_data)`: Analyzes the cleaned data to extract yearly temperature trends.
- **Technologies**: Relies on `pandas` and `numpy` for data analysis.

### `detect_top5_temperature_changes.py`
- **Purpose**: This script detects the top 5 years with the most significant temperature changes.
- **Key Functions**:
  - `detect_top5_changes(yearly_data)`: Identifies and returns the top 5 years with the highest temperature changes.
- **Technologies**: Uses `numpy` and `pandas` for statistical calculations and analysis.

### `data_viz.py`
- **Purpose**: This script is used for visualizing the temperature data trends and significant changes using line plots and bar charts.
- **Key Functions**:
  - `plot_temperature_trends(data)`: Plots the yearly temperature trends using a line plot.
  - `plot_top5_changes(data)`: Plots the top 5 temperature changes using a bar chart.
- **Technologies**: Uses `matplotlib.pyplot` for plotting.

![first](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/blob/SamePinchy-patch-1/assets/1.png?raw=true)
![second](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/blob/SamePinchy-patch-1/assets/2.png?raw=true)
![third](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/blob/SamePinchy-patch-1/assets/3.png?raw=true)
![fourth](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/blob/SamePinchy-patch-1/assets/4.png?raw=true)
![fifth](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/blob/SamePinchy-patch-1/assets/5.png?raw=true)

---

## Conclusion

This project aimed to analyze temperature data to identify significant changes over the years. Despite challenges with data cleaning and integration, the scripts work together to download, clean, analyze, and detect key trends in temperature changes. This documentation serves as a comprehensive guide to the project's progress, challenges, outcomes, and code functionality.

---
