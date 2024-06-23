import io
import logging
import os
import zipfile

import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(zip_url, directory):
    """
    Fetch a zip and extract it from a specified url to a specified directory

    :param zip_url: the url of the zipfile
    :param directory: the directory name of the extracted zip
    """
    try:
        logging.info(f"Fetching data from {zip_url}")
        response = requests.get(zip_url)
        response.raise_for_status()

        # unpack zipfile
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(directory)

        logging.info(f"Data fetched and saved to {directory}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching original_data: {e} \n Program will exit")
        exit()


def format_data(original_dir, new_dir):
    """
    Creates a new directory and fills it with just measurement data of the original dir. (Works only with temperature in the ECA data)

    :param original_dir: source directory filled with ECA temperature data
    :param new_dir: destination directory for the current type of measurement.
    """
    os.makedirs(new_dir, exist_ok=True)
    logging.info(f"Formatting data from {original_dir} to {new_dir}")

    files = [f for f in os.listdir(original_dir) if f.startswith("T")]
    total_files = len(files)
    for i, filename in enumerate(files):
        filepath = os.path.join(original_dir, filename)
        filename = filename[9:]
        filename = os.path.splitext(filename)[0]
        filename = str(int(filename))

        destination = os.path.join(new_dir, filename)

        convert_to_csv(filepath, destination, 20)
        
        progress = ((i + 1) / total_files) * 100
        logging.info(f"Formatting progress: {progress:.2f}%")

    logging.info(f"Finished formatting data and saved to {new_dir}")


def convert_to_csv(original_file, new_file, lines_to_skip=0):
    """
    Copy data from original file to a new file while skipping the specified number of lines and changing extension to csv.

    :param original_file: original file address
    :param new_file: new file address
    :param lines_to_skip: number of lines to skip from original file
    """

    base = os.path.splitext(new_file)[0]
    new_file = base + ".csv"
    try:
        logging.info(f"Converting {original_file} to {new_file}")
        with open(original_file, "r", encoding="utf8", errors="ignore") as file:
            lines = file.readlines()
        with open(new_file, "w", encoding="utf8", errors="ignore") as file:
            file.writelines(lines[lines_to_skip:])
        logging.info(f"Successfully converted {original_file} to {new_file}")
    except Exception as e:
        logging.error(f"Failed to convert file {original_file}: {e}")


def download_main(base_folder):
    # data source urls
    mean_url = "https://knmi-ecad-assets-prd.s3.amazonaws.com/download/ECA_blend_tg.zip"
    min_url = "https://knmi-ecad-assets-prd.s3.amazonaws.com/download/ECA_blend_tn.zip"
    max_url = "https://knmi-ecad-assets-prd.s3.amazonaws.com/download/ECA_blend_tx.zip"
    urls = [mean_url, min_url, max_url]
    subdirs = ["mean", "min", "max"]

    ECA_directory = "original_data"
    csv_data_dir = "csv_data"
    stations_csv = "stations.csv"

    # download and format all data
    total_steps = len(urls) * 2 + 1  # 2 steps for each type of data (fetch and format), plus 1 step for stations
    completed_steps = 0

    for i in range(3):
        temp = os.path.join(base_folder, ECA_directory, subdirs[i])
        dest = os.path.join(base_folder, csv_data_dir, subdirs[i])
        if not os.path.exists(temp):
            fetch_data(urls[i], temp)
            completed_steps += 1
            logging.info(f"Overall progress: {((completed_steps / total_steps) * 100):.2f}%")
            
            format_data(temp, dest)
            completed_steps += 1
            logging.info(f"Overall progress: {((completed_steps / total_steps) * 100):.2f}%")
        else:
            logging.info(f"Original {temp} dir already exists. Skipping")

    # create a stations csv file for station locations.
    source = os.path.join(base_folder, ECA_directory, subdirs[0], "stations.txt")
    stations_path = os.path.join(base_folder, stations_csv)
    convert_to_csv(source, stations_path, 17)
    completed_steps += 1
    logging.info(f"Overall progress: {((completed_steps / total_steps) * 100):.2f}%")

if __name__ == "__main__":
    folder = os.path.join(".")
    download_main(folder)
