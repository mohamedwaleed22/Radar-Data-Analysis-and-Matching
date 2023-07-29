import pandas as pd
import numpy as np
from datetime import datetime
import glob
from pathlib import Path
from tqdm import tqdm
# device = '/gpu:0' if tf.config.list_physical_devices('GPU') else '/cpu:0'
# with tf.device(device_name=device):

# pip install xlrd


# Fourth Script
def match(path1, path2):
    """
    arg*:
    path1: .xls files
    path2: .csv files
    f_path1 = path for matched file
    """
    f_path1 = str(input("Please include / within the path of matched File and the extension .csv: "))
    fixed_h = float(input("Please Enter Fixed Height as a decimal number: "))

    time_diffrence = str(input("Please specify Time Difference in minutes and seconds as MM:SS "))
    mints = int(time_diffrence.split(':')[0])
    secnds = int(time_diffrence.split(':')[1])
    abs_diff_sec = (mints * 60) + secnds

    lat_lon_diff = float(input("Please specify Latitude and Longitude Difference in float format "))
    altitude_diff = float(input("Please specify Altitude Difference in float format "))

    filepath1 = Path(f_path1)
    filepath1.parent.mkdir(parents=True, exist_ok=True)
    # read .xls files and appending them into DataFrame object
    xls_files = glob.glob(path1 + "/*.xls")
    df_list = (pd.read_excel(file, header=None, skiprows=2) for file in xls_files)
    big_df = pd.concat(df_list, ignore_index=True)
    big_df = big_df.rename(columns={2: 'Date', 3: 'HeightMSL', 4: 'Speed', 5: 'Dir', 6: 'Lat', 7: 'Lon'})
    big_df = big_df.drop(big_df[(big_df['Lat'] == '//////') & (big_df['Lon'] == '//////')].index, axis=0)
    big_df['Date'] = big_df['Date'].astype(str).str[:19]

    # read .csv files and appending them into DataFrame object
    csv_files = glob.glob(path2 + "/*.csv")
    df_list2 = (pd.read_csv(file) for file in csv_files)
    big_df2 = pd.concat(df_list2, ignore_index=True)
    big_df2 = big_df2.dropna(axis=1)

    df_final = pd.DataFrame(
        columns=["Lat", "Long", "Alt", "Date", "SpeedUP", "SpeedWR", "DirUp"], index=[0])

    # loop through .xls files DataFrame
    for z in tqdm(range(0, len(big_df))):
        upper_date = big_df.iloc[z]['Date']

        # loop through row: i, col: j in the .csv files DataFrame
        if upper_date == 'NaT' or upper_date == 'nat':
            continue
        else:
            dateFinalUp = datetime.strptime(upper_date, '%Y-%m-%d %H:%M:%S')
            upper_long = big_df.iloc[z]['Lon']
            upper_lat = big_df.iloc[z]['Lat']
            upper_alt = big_df.iloc[z]['HeightMSL']
            upper_alt = upper_alt + fixed_h
            DirUp = big_df.iloc[z]['Dir']
            SpeedUp = big_df.iloc[z]['Speed']

            for i in range(0, len(big_df2)):
                y = big_df2.iat[i, 0]
                date_ = y.split(',')[5].split(':')[1:]
                date = (":".join(str(i).strip(' ') for i in date_))
                dateFinalWR = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                delta_1 = abs(dateFinalUp - dateFinalWR)
                time_df = delta_1.total_seconds()

                if time_df > abs_diff_sec:
                    continue
                else:

                    for j in range(0, big_df2.shape[1]):
                        x = big_df2.iat[i, j]
                        Long = "{}".format(str(x.split(',')[3].split(':')[1].strip(' ')))
                        Lat = "{}".format(str(x.split(',')[2].split(':')[1].strip(' ')))
                        alt = "{}".format(str(x.split(',')[4].split(':')[1].strip(' ')))
                        speedWR = "{}".format(str(x.split(',')[6].split(':')[1].strip(' ')))
                        date_1 = x.split(',')[5].split(':')[1:]
                        date1 = (":".join(str(i).strip(' ') for i in date_1))
                        dateFinalWR1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
                        delta_1 = abs(dateFinalUp - dateFinalWR1)
                        time_df1 = delta_1.total_seconds()
                        if time_df1 <= abs_diff_sec:

                            # Calculating Error Difference

                            lat_diff = abs(float(upper_lat) - float(Lat))
                            long_diff = abs(float(Long) - float(upper_long))
                            alt_diff = abs(float(upper_alt) - float(alt))

                            # Querying through matched records and Adding them into a .csv file

                            if (lat_diff <= lat_lon_diff) and (long_diff <= lat_lon_diff) and \
                                    (alt_diff <= altitude_diff):

                                row2 = pd.Series({"Lat": Lat, "Long": Long, "Alt": alt, "Date": dateFinalWR1, "SpeedUP": SpeedUp,
                                     "SpeedWR": speedWR, "DirUp": DirUp})
                                df_final = pd.concat([df_final, row2.to_frame().T], ignore_index=True)
                                df_final['D_WR'] = 0
    df_final.to_csv(filepath1)



# example input: C:/Users/dell g3/PycharmProjects/Z_files
# matching files function
match(path1=str(input("please include / within .xls path1: ")), path2=str(input("please include / within .csv path2: ")))
print("Finished Processing files")
