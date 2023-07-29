import pandas as pd
import numpy as np
from datetime import datetime
import glob
from pathlib import Path
# pip install xlrd
from tqdm import tqdm
# device = '/gpu:0' if tf.config.list_physical_devices('GPU') else '/cpu:0'
# with tf.device(device_name=device):



# Second Script
def phenom(path):
    """
        arg*:
        path: .csv files
        f_path1 = path of created z file
        """
    f_path1 = str(input("Please include / within the path of Z File and the extension .csv: "))
    filepath1 = Path(f_path1)
    filepath1.parent.mkdir(parents=True, exist_ok=True)
    # read .csv files and appending them into DataFrame object
    csv_files = glob.glob(path + "/*.csv")
    df_list2 = (pd.read_csv(file, skip_blank_lines=True, na_filter=False) for file in csv_files)
    big_df2 = pd.concat(df_list2, ignore_index=True)

    df_Z = pd.DataFrame(columns=["Lat", "Long", "Alt", "Date", "SpeedWR", "Z", "Phenomena"],
                        index=[0])

    # loop through row: i, col: j in the .csv files DataFrame
    for i in tqdm(range(0, len(big_df2))):
        for j in range(0, big_df2.shape[1]):
            x = big_df2.iat[i, j]
#             if x == 'nan' or x == np.NaN or x == 'NaN':
#                 continue
            Long = "{}".format(str(x.split(',')[3].split(':')[1].strip(' ')))
            Lat = "{}".format(str(x.split(',')[2].split(':')[1].strip(' ')))
            alt = "{}".format(str(x.split(',')[4].split(':')[1].strip(' ')))
            date_ = x.split(',')[5].split(':')[1:]
            date = (":".join(str(i).strip(' ') for i in date_))
            speedWR = "{}".format(str(x.split(',')[6].split(':')[1].strip(' ')))
            Z = "{}".format(str(x.split(',')[9].split(':')[1].strip(' ')))
            dateFinalWR = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

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
                    {"Lat": Lat, "Long": Long, "Alt": alt, "Date": dateFinalWR, "SpeedWR": speedWR, "Z": Z,
                     "Phenomena": phenomena})
                df_Z = pd.concat([df_Z, row.to_frame().T], ignore_index=True)
    df_Z.to_csv(filepath1)


# example input: C:/Users/dell g3/PycharmProjects/Task_Air

# phenomena function
phenom(path=str(input("Please include / within the path of .csv files: ")))
print("Finished Processing files")
