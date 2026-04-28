import pandas as pd
from pathlib import Path
import numpy as np
from scipy.io import wavfile
import os


# ------------------------------------------------------------- #
def getSexAgeDict(excel_path, groups):
    dic = {}

    for group in groups:
        df = pd.read_excel(excel_path, sheet_name=group, header=0, nrows=42)
        df["Code"] = df["Code"].astype(str).str.strip()
        df["Sex"]  = df["Sex"].astype(str).str.strip()
        df["Age"]  = pd.to_numeric(df["Age"], errors="coerce")

        for code, sex, age in zip(df["Code"], df["Sex"], df["Age"]):
            dic[code] = (sex, age)

    return dic

def getSubharms(csv_path):
    if not os.path.isfile(csv_path):
        return None
    
    df = pd.read_csv(csv_path)        

    subharms = []

    a = False
    counter = 0
    for _, row in df.iterrows():
        counter += 1
        if row["text"] == "a":
            interval = (float(row["tmin"]), float(row["tmax"]))
            subharms.append(interval)
            a = True

    if counter > 1 and not a:
        print(f"---- PROBLEM WITH {csv_path}")

    return subharms

# SUBHARMONICS DURATION : SIGNAL DURATION RATIO
def subharmRatio(subharm_total_no : int, subharms, data, sample_rate):
    subharm_ratio = 0.
    subharm_per_second = 0.
    subharm_durations = []

    density_slope = 0.
    pct_subharm_num_second_half = 0.
    dur_density_slope = 0.
    pct_subharm_dur_second_half = 0.

    if subharm_total_no > 0:
        subharm_durations = [b - a for a, b in subharms]
        signal_duration = len(data)/sample_rate

        total_subharm_dur = sum(subharm_durations)
        subharm_ratio = total_subharm_dur/signal_duration
        subharm_per_second = subharm_total_no / signal_duration

        # Second half features
        half_time = signal_duration / 2.0
        n_second = sum(1 for (a, b) in subharms if a >= half_time)
        n_first = subharm_total_no - n_second

        pct_subharm_num_second_half = n_second/subharm_total_no
        density_slope = (n_second - n_first)/half_time

        subharm_dur_second = 0.0
        for a, b in subharms:
            subharm_dur_second += max(0.0, b - max(a, half_time))
        subharm_dur_first = total_subharm_dur - subharm_dur_second

        pct_subharm_dur_second_half = subharm_dur_second / total_subharm_dur
        dur_density_slope = (subharm_dur_second - subharm_dur_first)/half_time

    return subharm_ratio, subharm_per_second, subharm_durations, density_slope, pct_subharm_num_second_half, dur_density_slope, pct_subharm_dur_second_half

# FIRST SUBHARMONIC OCCURENCE
def firstSubharmOccur(subharm_total_no, subharms, data, sample_rate):
    first_subharm_occur = len(data)/sample_rate
    if subharm_total_no > 0:
        first_subharm_occur = subharms[0][0]
    
    return first_subharm_occur

# MEAN / MEDIAN / STD / CV SUBHARMONIC DURATION
def statsSubharmDur(subharm_total_no, subharm_durations):
    avg_subharm_dur, median_subharm_dur, std_subharm_dur, coeffOfVar_subharm_dur, longest_subharm_dur = 0., 0., np.nan, np.nan, 0.

    if subharm_total_no > 0:
        avg_subharm_dur = np.mean(subharm_durations)
        median_subharm_dur = np.median(subharm_durations)

        if subharm_total_no > 1: # at least 2 subharmonics for std calculation
            std_subharm_dur = np.std(subharm_durations, ddof=1)
            coeffOfVar_subharm_dur = std_subharm_dur / avg_subharm_dur

        longest_subharm_dur = np.max(subharm_durations)

    return avg_subharm_dur, median_subharm_dur, std_subharm_dur, coeffOfVar_subharm_dur, longest_subharm_dur


# INTER-SUBHARMONIC INTERVALS 
def interSubharmIntervals(subharm_total_no, subharms):

    mean_intervals, median_intervals, std_intervals, COV_intervals = np.nan, np.nan, np.nan, np.nan

    if subharm_total_no > 1: # at least 2 subharmonics for an interval
        inter_intervals = subharms[1:, 0] - subharms[:-1, 1]

        mean_intervals = np.mean(inter_intervals)
        median_intervals = np.median(inter_intervals)

        if subharm_total_no > 2: # at least 2 intervals for std calculation
            std_intervals = np.std(inter_intervals, ddof=1)
            COV_intervals = std_intervals / mean_intervals

    return mean_intervals, median_intervals, std_intervals, COV_intervals


# ------------------------------------------------------------- #

groups = ["HC", "RBD", "PN", "MSA"]
result_rows = []
subharm_rows = []

excel_path = "Databaze_subharmonicke_09.06.2025.xlsx"
dic = getSexAgeDict(excel_path, groups)

for group in groups:

    folder_path = Path(group)/"prodlouzena_fonace"

    if folder_path.exists():
        for file_path in folder_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == ".wav":

                sample_rate, data = wavfile.read(file_path)
                sample_name = file_path.stem

                csv_path = "labels/" + group + "/" + sample_name + ".csv"


                # Extract subharmonics
                subharms = getSubharms(csv_path)
                subharms = np.asarray(subharms, dtype=float)

                if subharms is None:
                    continue
                # print(subharms)

                # ABSOLUTE NUMBER OF SUBHARMONICS IN THE SIGNAL
                subharm_total_no = len(subharms)
                # print(f"TOTAL NO. OF SUBHARMONICS: {subharm_total_no}")

                # SUBHARMONICS DURATION : SIGNAL DURATION RATIO
                subharm_ratio, subharm_per_second, subharm_durations, density_slope, pct_subharm_num_second_half, dur_density_slope, pct_subharm_dur_second_half = subharmRatio(subharm_total_no, subharms, data, sample_rate)
                # print(f"SUBHARMONICS-SIGNAL RATIO: {subharm_ratio}")

                subharm_durations = np.asarray(subharm_durations, dtype=float)

                # FIRST SUBHARMONIC OCCURENCE
                first_subharm_occur = firstSubharmOccur(subharm_total_no, subharms, data, sample_rate)
                # print(f"SUBHARMONIC FIRST OCCURENCE: {first_subharm_occur} seconds")

                # SUBHARMONIC DURATION STATS
                avg_subharm_dur, median_subharm_dur, std_subharm_dur, coeffOfVar_subharm_dur, longest_subharm_dur = statsSubharmDur(subharm_total_no, subharm_durations)
                # print(f"AVERAGE SUBHARMONIC DURATION: {avg_subharm_dur} seconds")    

                # INTER-SUBHARMONIC INTERVALS      
                mean_intervals, median_intervals, std_intervals, COV_intervals = interSubharmIntervals(subharm_total_no, subharms)

                if group == "RBD":
                    sex, age = dic[sample_name[:6]][0], dic[sample_name[:6]][1]
                else:
                    sex, age = dic[sample_name[:5]][0], dic[sample_name[:5]][1]

                result_rows.append(
                    (sample_name, sex, age, group,
                    subharm_total_no, 
                    subharm_ratio, subharm_per_second,
                    density_slope, pct_subharm_num_second_half, dur_density_slope, pct_subharm_dur_second_half,
                    first_subharm_occur, 
                    avg_subharm_dur, median_subharm_dur, std_subharm_dur, coeffOfVar_subharm_dur, longest_subharm_dur,
                    mean_intervals, median_intervals, std_intervals, COV_intervals))


                firstSubharm = True
                for subharm in subharms:
                    if not firstSubharm:
                        subharm_rows.append(("", "", subharm[0], subharm[1]))
                    else:
                        subharm_rows.append((sample_name, group, subharm[0], subharm[1]))
                        firstSubharm = False

                

df_results = pd.DataFrame(
    result_rows,
    columns=["sample", "sex", "age", "group", "subharm_num", "subharm_sig_ratio", "subharm_per_second",
    "density_num_slope", "pct_subharm_num_2nd_half", "density_dur_slope", "pct_subharm_dur_2nd_half",
    "first_occur", 
    "avg_dur", "median_dur", "std_dur", "CV_dur", "longest_dur",
    "mean_inter_intervals", "median_inter_intervals", "std_inter_intervals", "COV_inter_intervals"])

df_results.to_csv("results.csv", index=False)


df_subharms = pd.DataFrame(
    subharm_rows,
    columns=["sample", "group", "tmin", "tmax"]
)

df_subharms.to_csv("subharm_times.csv", index=False)

