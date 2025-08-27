import csv
from pathlib import Path
import numpy as np


def run_analysis(input_path: str, output_path: str):

    output_types = {"seasonal_averages": "average_temp.txt"
                    , "temperature_variance": "largest_temp_range_station.txt"
                    , "temperature_stability": "temperature_stability_stations.txt"}

    DELIMITER = ","

    SEASON_MONTHS_MASKS = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]]

    seasons = {
        "Spring": ["September", "October", "November"]
        , "Summer": ["December", "January", "February"]
        , "Autumn": ["March", "April", "May"]
        , "Winter": ["June", "July", "August"]
    }

    station_temperatures = read_csv_files(input_path, DELIMITER, SEASON_MONTHS_MASKS)

    seasonal_averages = get_seasonal_average(seasons, station_temperatures)
    temperature_range = get_temperature_range(station_temperatures)
    temperature_stability = get_station_temperature_stability(station_temperatures)

    for output_type, output_file_name in output_types.items():

        if output_type == "seasonal_averages":
            formatted_output = format_sa_output(seasonal_averages)
            write_to_file(Path(output_path) / output_file_name, formatted_output)

        elif output_type == "temperature_variance":
            formatted_output = format_temperature_range_output(temperature_range)
            write_to_file(Path(output_path) / output_file_name, formatted_output)

        elif output_type == "temperature_stability":
            formatted_output = format_temperature_stability_output(temperature_stability)
            write_to_file(Path(output_path) / output_file_name, formatted_output)

def write_to_file(output_path: str, data: list) -> None:

    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, mode="w") as f:
        for output_line in data:
            f.write(output_line)

def format_sa_output(data: dict) -> str:
    """
    Auto rounding of temp floats is done here using f-string.
    """
    return_strings = []

    for season, temp in data.items():
        return_strings.append(f"{season}: {temp:.1f}°C\n")

    return return_strings

def format_temperature_range_output(data: dict) -> str:
    """
    Auto rounding of temp floats is done here using f-string.
    """
    return_strings = []

    for min_max, stations in data.items():

        if min_max == "min":
            pass
        else:
            for (station_name, temp_variance, temp_min, temp_max) in stations:
                return_strings.append(f"{station_name}: Range {temp_variance:.1f} (Max: {temp_max:.1f}, Min: {temp_min:.1f})°C\n")
    
    return return_strings
    
def format_temperature_stability_output(data: dict) -> str:
    """
    Auto rounding of temp floats is done here using f-string.
    """
    return_strings = []

    for min_max, stations in data.items():

        if min_max == "min":
            for (station_name, temp_std_dev) in stations:
                return_strings.append(f"Most Stable: Station {station_name}: StdDev {temp_std_dev:.1f}°C\n")
        elif min_max == "max":
            for (station_name, temp_std_dev) in stations:
                return_strings.append(f"Most Variable: Station {station_name}: StdDev {temp_std_dev:.1f}°C\n")
    
    return return_strings

def read_csv_files(path: str, delimiter: str, season_months_masks) -> dict:
    station_temperatures = {}
    
    for csv_file in path.glob("*.csv"):

        for (idx, row) in enumerate(csv.reader(open(csv_file, mode="r"), delimiter=delimiter)):
            
            if idx == 0:
                # Skip headers
                continue
            else:

                # Here we are assuming all rows in all CSV files adhere to the same format.

                station_name, station_id = row[:2]
                month_temps = np.array(row[4:]).astype(float)

                seasons_container = []

                # Convert lists to numpy arrays and multiply
                for i in range(len(season_months_masks)):
                    season_temp_positions = np.nonzero(np.multiply(month_temps, season_months_masks[i]))

                    season_temps = month_temps[season_temp_positions].tolist()

                    seasons_container.append(season_temps)


                if station_temperatures.get(station_id) != None:

                    if seasons_container != []:

                        for i in range(len(season_months_masks)):
                            
                            # Station already exists, append new temps to existing list.
                            station_temperatures[station_id][1][i].extend(seasons_container[i])

                else:
                    station_temperatures[station_id] = (station_name, seasons_container)

    return station_temperatures

def get_seasonal_average(seasons: dict, station_temperatures: dict) -> dict:

    seasonal_averages = {
    }

    for idx, season in enumerate(seasons.keys()):
        temps_container = []

        for station_id, (station_name, seasons_container) in station_temperatures.items():

            temps_container.extend(seasons_container[idx])

        seasonal_averages[season] = np.mean(temps_container)

    return seasonal_averages

def get_temperature_range(station_temperatures: dict) -> dict:

    # (station_name, variance, min_temp, max_temp)
    min_variance = ()
    max_variance = ()

    min_variance_return = []
    max_variance_return = []

    for station_id, (station_name, seasons_container) in station_temperatures.items():

        station_container = []

        for temps in seasons_container:
            station_container.extend(temps)

        min_temp, max_temp = np.min(station_container), np.max(station_container)

        if max_variance == ():
            max_variance = (station_name, abs(max_temp - min_temp), min_temp, max_temp)
            max_variance_return.append(max_variance)
        if min_variance == ():
            min_variance = (station_name, abs(max_temp - min_temp), min_temp, max_temp)
            min_variance_return.append(min_variance)

        if abs(max_temp - min_temp) > max_variance[1]:
            max_variance = (station_name, abs(max_temp - min_temp), min_temp, max_temp)
            max_variance_return.clear()
            max_variance_return.append(max_variance)
        elif abs(max_temp - min_temp) == max_variance[1]:
            max_variance_return.append((station_name, abs(max_temp - min_temp), min_temp, max_temp))

        if abs(max_temp - min_temp) < min_variance[1]:
            min_variance = (station_name, abs(max_temp - min_temp), min_temp, max_temp)
            min_variance_return.clear()
            min_variance_return.append(min_variance)
        elif abs(max_temp - min_temp) == min_variance[1]:
            min_variance_return.append((station_name, abs(max_temp - min_temp), min_temp, max_temp))

    return {"min": min_variance_return
    , "max": max_variance_return
    }

def get_station_temperature_stability(station_temperatures: dict) -> dict:
    min_stdev = ()
    max_stdev = ()

    min_stdev_return = []
    max_stdev_return = []

    for station_id, (station_name, seasons_container) in station_temperatures.items():

        station_container = []

        for temps in seasons_container:
            station_container.extend(temps)

        station_stdev = np.std(np.array(station_container))

        if min_stdev == ():
            min_stdev = (station_name, station_stdev)
            min_stdev_return.append(min_stdev)
        elif station_stdev < min_stdev[1]:
            min_stdev = (station_name, station_stdev)
            min_stdev_return.clear()
            min_stdev_return.append(min_stdev)
        elif station_stdev == min_stdev[1]: 
            min_stdev_return.append((station_name, station_stdev))

        if max_stdev == ():
            max_stdev = (station_name, station_stdev)
            max_stdev_return.append(max_stdev)
        elif station_stdev > max_stdev[1]:
            max_stdev = (station_name, station_stdev)
            max_stdev_return.clear()
            max_stdev_return.append(max_stdev)
        elif station_stdev == max_stdev[1]:
            max_stdev_return.append((station_name, station_stdev))
        


    return {"min": min_stdev_return
    , "max": max_stdev_return
    }
    

if __name__ == "__main__":
    path_to_csvs = Path(input("Please enter the path to the folder containing the CSV files: "))
    output_path = input("Please enter the path to the output folder: ")

    run_analysis(path_to_csvs, output_path)