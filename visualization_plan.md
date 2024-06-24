## **Visualization Plan Document**

### **Introduction**

1. **Purpose of the visualizations:**

The purpose of visualizations is to analyze and depict temperature trends in Europe over recent decades, highlighting significant changes and differences between various regions.

1. **Overview of the data being visualized:**

The data consists of temperature records (minimum, mean, maximum) from the European Climate Assessment & Dataset (ECA&D). The records span from 1980 to the present and include temperature measurements from 23759 various stations across Europe.

### **Plot Types and Descriptions**

**Line Plot:**

- **Purpose:** To show temperature trends over time for selected areas.
- **X-Axis:** Time
- **Y-Axis:** Temperature (°C)
- **Details:** Each line represents a different area, showing how temperatures have changed over time.
- **Implementation Proposal:** User can manually select the region of interest clicking on the map of Europe. The program will read which station is located the closest basing on longitude and latitude of the place clicked. Then will appear 3 line plots of temperature trends (max,mean,min) based on sensor readings of a station.

**Bar Chart:**

- **Purpose:** To compare temperature changes between different areas.
- **X-Axis:** Selected Areas
- **Y-Axis:** Temperature Change (°C)
- **Details:** Bars represent the magnitude of mean temperature change for each area, allowing easy comparison between regions.
- **Implementation Proposal:** The user will be able to manually select 5 regions on the map. Upon clicking, the program will locate the nearest station, and its collected results will be displayed on a chart. Clicking on the station again will cancel its selection. This chart will allow for a more detailed analysis of temperature differences across various regions.

**Heatmap:**

- **Purpose:** To visualize temperature changes across a geographic grid.
- **X-Axis:** Longitude
- **Y-Axis:** Latitude
- **Details:** Colors represent the degree of temperature change, providing a spatial understanding of temperature variations.
- **Implementation Proposal:** Every station will create a radius of ,,x” kilometers. Then a difference between first and last mean temperature value from sensor will be calculated and depending on a result, the proper color will cover the circle.

### **Axis Configurations**

**Line Plot:**

- **X-Axis:**
  - **Data:** Time (Years)
  - **Range:** Variable based on data from sensor
  - **Scale:** Linear
  - **Label:** "Year"
- **Y-Axis:**
  - **Data:** Temperature (°C)
  - **Range:** Variable based on data from sensor
  - **Scale:** Linear
  - **Label:** "Temperature (°C)

**Bar Chart:**

- **X-Axis:**
  - **Data:** Areas
  - **Type:** Categorical
  - **Label:** "Regions"
- **Y-Axis:**
  - **Data:** Temperature Change (°C)
  - **Range:** Variable based on data
  - **Scale:** Linear
  - **Label:** "Temperature Change (°C)"

**Heatmap:**

- **X-Axis:**
  - **Data:** Longitude
  - **Range:** Based on dataset
  - **Scale:** Linear
  - **Label:** "Longitude"
- **Y-Axis:**
  - **Data:** Latitude
  - **Range:** Based on dataset
  - **Scale:** Linear
  - **Label:** "Latitude”

### **Data Queries**

**Line Plot Data Query:**
![Zrzut ekranu 2024-06-24 230110](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/assets/108231926/051dddc3-0fb7-4eca-a5b1-9fa6a38979cc)

Bar Chart Data Query:
![Zrzut ekranu 2024-06-24 230156](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/assets/108231926/f0841b10-d990-4c76-84ae-daed96954182)

Heatmap Data Query:
![Zrzut ekranu 2024-06-24 230220](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/assets/108231926/305eaa7a-dfc6-405d-ba79-8566cdccbc55)

Other Helpful Querries:

Receiving Station ID closest to clicked on map
![Zrzut ekranu 2024-06-24 230248](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/assets/108231926/5cc20111-5f12-405d-9119-f6b4d63be031)

Receiving date and temperature (depending on which one is needed - max,min,mean):
![Zrzut ekranu 2024-06-24 230318](https://github.com/D-Mielewczyk/euro-temperature-trend-stats/assets/108231926/ec19977f-5151-4841-9481-cf5eef57b3f4)

The example code for handling mouse press and creating a simple Europe map will be included.

### **Conclusion**

**Summary of the visualization plan:** This document outlines the plan for visualizing temperature trends in Europe, including the types of plots to be used, axis configurations, and data queries. The visualizations aim to provide clear insights into temperature changes over time and across different regions.

**Next steps and considerations for implementation:**

- Implement the data extraction and transformation queries.
- Develop the visualizations using a suitable plotting library (e.g., Matplotlib, Seaborn).
- Ensure the visualizations are integrated into the project and available on the GitHub repository.
- Update the documentation as needed based on feedback and additional requirements.
