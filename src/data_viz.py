import plotly.graph_objects as go
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Function to recursively load CSV files from nested directories and add STAID
def load_processed_data_with_staid(folder_path):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                # Extract STAID from the directory name
                staid = int(os.path.basename(root).split('=')[-1])
                df = pd.read_csv(file_path)
                df['STAID'] = staid  # Add the extracted STAID to the DataFrame
                all_files.append(df)
    if all_files:
        return pd.concat(all_files, ignore_index=True)
    else:
        return pd.DataFrame()

# Loading data from the new structure
min_temp_df = load_processed_data_with_staid("line_plot_data/min")
mean_temp_df = load_processed_data_with_staid("line_plot_data/mean")
max_temp_df = load_processed_data_with_staid("line_plot_data/max")



# Loading station data
stations_df = pd.read_csv("stations.csv")

# Function to convert DMS to DD
def dms_to_dd(dms_str):
    dms_str = dms_str.strip()
    direction = dms_str[0]
    dms = list(map(float, dms_str[1:].split(":")))
    dd = dms[0] + dms[1] / 60 + dms[2] / 3600
    if direction in ['S', 'W']:
        dd *= -1

    return dd

# Clean up column names by stripping whitespace


stations_df.columns = stations_df.columns.str.strip()


# Apply coordinate conversion


stations_df['LAT'] = stations_df['LAT'].apply(dms_to_dd)
stations_df['LON'] = stations_df['LON'].apply(dms_to_dd)




stations_df['STAID'] = stations_df['STAID'].astype(int)




# Function to add geo coordinates to DataFrame
def add_geo_coordinates(df, stations_df):
    return df.merge(stations_df[['STAID', 'LAT', 'LON']], on='STAID', how='left')

# Add geo coordinates to temperature data
min_temp_df = add_geo_coordinates(min_temp_df, stations_df)
mean_temp_df = add_geo_coordinates(mean_temp_df, stations_df)
max_temp_df = add_geo_coordinates(max_temp_df, stations_df)

# Function to create a single line plot for a given temperature dataframe
#When there are multiple STAID it only keep first so that line plots are only made for one station as it was supposed to be
def create_single_line_plot(df, temp_type, name):
    # Filter to use only the first occurrence of each STAID
    df_filtered = df.drop_duplicates(subset=['STAID'], keep='first')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtered['YEAR'], y=df_filtered[temp_type], mode='lines',
                             name=f'{temp_type.capitalize()} Temp'))
    fig.update_layout(title=f'{name} Temperature Trends Over Time',
                      xaxis_title='Year',
                      yaxis_title='Temperature (°C)')


    
    fig.write_html(f"{name}_line_plot.html")

    fig.show()
# Create individual plots for min, mean, and max temperatures
create_single_line_plot(min_temp_df, 'TN','Min')
create_single_line_plot(mean_temp_df, 'TG','Mean')
create_single_line_plot(max_temp_df, 'TX','Max')


# Bar chart function
def create_bar_chart(df):

    temp_change_df = df.groupby('STAID').agg({'TG': lambda x: x.max() - x.min()}).reset_index()
    temp_change_df.columns = ['STAID', 'Temperature Change (°C)']
    fig = px.bar(temp_change_df, x='STAID', y='Temperature Change (°C)', title='Temperature Changes by Region')
    fig.update_layout(xaxis_title='Regions', yaxis_title='Temperature Change (°C)')

    # Save as HTML and open in browser
    fig.write_html("bar_chart.html")


    # Show using plotly.io.show method for better display in various environments
    pio.show(fig, renderer="browser")  # or renderer="iframe" depending on preference




#
def create_heatmap(df):


    # Add debug prints to check data


    df['Temperature Change'] = df.groupby('STAID')['TG'].transform(lambda x: x.max() - x.min())


    fig = px.density_mapbox(df, lat='LAT', lon='LON', z='Temperature Change', radius=10,
                            center=dict(lat=50, lon=10), zoom=3,
                            mapbox_style="carto-positron",color_continuous_scale="Viridis")

    fig.update_layout(title='Temperature Changes Across Geographic Grid',
                      xaxis_title='Longitude',
                      yaxis_title='Latitude', coloraxis_colorbar=dict(title='Temperature Change (°C)'))
    fig.write_html("heatmap.html")
    fig.show()




# Wywołanie funkcji create_heatmap


create_bar_chart(mean_temp_df)
create_heatmap(mean_temp_df)

