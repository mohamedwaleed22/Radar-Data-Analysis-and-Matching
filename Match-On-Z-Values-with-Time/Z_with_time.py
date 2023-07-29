import pandas as pd
import numpy as np
from datetime import datetime
import glob
from pathlib import Path
from tqdm import tqdm

# device = '/gpu:0' if tf.config.list_physical_devices('GPU') else '/cpu:0'
# with tf.device(device_name=device):


# Second Script
def phenom(path):
    """
        arg*:
        path: .csv files
        f_path1 = path of created Z file
        """
    f_path1 = str(input("Please include / within the path of Z File and the extension .csv: "))
    filepath1 = Path(f_path1)
    filepath1.parent.mkdir(parents=True, exist_ok=True)
    # read .csv files and appending them into DataFrame object
    csv_files = glob.glob(path + "/*.csv")
    df_list2 = (pd.read_csv(file, skip_blank_lines=True, na_filter=False) for file in csv_files)
    big_df2 = pd.concat(df_list2, ignore_index=True)
    # Date range inputs
    date1_components = input('Enter the first date formatted as YYYY-MM-DD ').split('-')
    time1_components = input('Enter the first time formatted as HH:MM:SS ').split(':')
    year1, month1, day1 = [int(item) for item in date1_components]
    hours1, minutes1, seconds1 = [int(item) for item in time1_components]
    dt_1 = datetime(year=year1, month=month1, day=day1, hour=hours1, minute=minutes1, second=seconds1)
    date2_components = input('Enter the second date formatted as YYYY-MM-DD ').split('-')
    time2_components = input('Enter the second time formatted as HH:MM:SS ').split(':')
    year2, month2, day2 = [int(item) for item in date2_components]
    hours2, minutes2, seconds2 = [int(item) for item in time2_components]
    dt_2 = datetime(year=year2, month=month2, day=day2, hour=hours2, minute=minutes2, second=seconds2)

    df_Z = pd.DataFrame(columns=["Lat", "Long", "Alt", "Date", "SpeedWR", "Z", "Phenomena"],
                        index=[0])

    # loop through row: i, col: j in the .csv files DataFrame
    for i in tqdm(range(0, len(big_df2))):
        y = big_df2.iat[i, 0]
        date_ = y.split(',')[5].split(':')[1:]
        date = (":".join(str(i).strip(' ') for i in date_))
        dateFinalWR = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if dt_1 <= dateFinalWR <= dt_2:

            for j in range(0, big_df2.shape[1]):
                x = big_df2.iat[i, j]
                Long = "{}".format(str(x.split(',')[3].split(':')[1].strip(' ')))
                Lat = "{}".format(str(x.split(',')[2].split(':')[1].strip(' ')))
                alt = "{}".format(str(x.split(',')[4].split(':')[1].strip(' ')))
                speedWR = "{}".format(str(x.split(',')[6].split(':')[1].strip(' ')))
                Z = "{}".format(str(x.split(',')[9].split(':')[1].strip(' ')))
                date_1 = x.split(',')[5].split(':')[1:]
                date1 = (":".join(str(i).strip(' ') for i in date_1))
                dateFinalWR1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
                if dt_1 <= dateFinalWR1 <= dt_2:

                    phenomena = str()
                    if Z == np.NAN or Z == 'nan' or Z == 'NaN':
                        continue
                    elif float(Z) >= 20 and float(Z) <= 30:
                        phenomena = 'Showers Thunder,Rain, Altostratus Clouds'
                    elif float(Z) >= -8 and float(Z) < 12:
                        phenomena = 'Altostratus Clouds'
                    elif float(Z) > 40 and float(Z) <= 60:
                        phenomena = 'Showers Thunder'
                    elif float(Z) >= 12 and float(Z) < 20:
                        phenomena = 'Rain, Altostratus Clouds'
                    elif float(Z) > 30 and float(Z) <= 40:
                        phenomena = 'Showers Thunder, Rain'
                    else:
                        phenomena = 'other'

                    # Adding Z, Phenomena in a separate .csv file
                    if float(Z) >= -8 and float(Z) <= 60:
                        row = pd.Series(
                            {"Lat": Lat, "Long": Long, "Alt": alt, "Date": dateFinalWR1, "SpeedWR": speedWR, "Z": Z,
                             "Phenomena": phenomena})
                        df_Z = pd.concat([df_Z, row.to_frame().T], ignore_index=True)
    df_Z.to_csv(filepath1)


# example input: C:/Users/dell g3/PycharmProjects/Task_Air
# phenomena function
phenom(path=str(input("Please include / within the path of .csv files: ")))
print("Finished Processing files")
