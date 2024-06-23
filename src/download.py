import io
import os
import zipfile

import requests


def fetch_data(zip_url, directory):
    """
    Fetch a zip and extract it from a specified url to a specified directory

    :param zip_url: the url of the zipfile
    :param directory: the directory name of the extracted zip
    """
    try:
        response = requests.get(zip_url)
        response.raise_for_status()

        # unpack zipfile
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(directory)

        print(f"Data fetched and saved to {directory}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching original_data: {e} \n Program will exit")
        exit()


def format_data(original_dir, new_dir):
    """
    Creates a new directory and fills it with just measurement data of the original dir. (Works only with temperature in the ECA data)

    :param original_dir: source directory filled with ECA temperature data
    :param new_dir: destination directory for the current type of measurement.
    """
    os.makedirs(new_dir, exist_ok=True)

    for filename in os.listdir(original_dir):
        if filename.startswith("T"):
            filepath = os.path.join(original_dir, filename)
            filename = filename[9:]
            filename = os.path.splitext(filename)[0]
            filename = str(int(filename))

            destination = os.path.join(new_dir, filename)

            convert_to_csv(filepath, destination, 20)
    print(f"Finished formatting data and saved to {new_dir}")


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
        with open(original_file, "r", encoding="utf8", errors="ignore") as file:
            lines = file.readlines()
        with open(new_file, "w", encoding="utf8", errors="ignore") as file:
            file.writelines(lines[lines_to_skip:])
    except Exception as e:
        print(f"Failed to convert file: {e}")


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
    for i in range(3):
        temp = os.path.join(base_folder, ECA_directory, subdirs[i])
        dest = os.path.join(base_folder, csv_data_dir, subdirs[i])
        if not os.path.exists(temp):
            fetch_data(urls[i], temp)
            # convert to csv
            format_data(temp, dest)
        else:
            print(f"Original {temp} dir already exists. Skipping")

    # create a stations csv file for station locations.
    source = os.path.join(base_folder, ECA_directory, subdirs[0], "stations.txt")
    stations_path = os.path.join(base_folder, stations_csv)
    convert_to_csv(source, stations_path, 17)


if __name__ == "__main__":
    folder = os.path.join(".")
    download_main(folder)
