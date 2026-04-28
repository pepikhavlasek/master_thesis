from pathlib import Path
import numpy as np
from scipy.io import wavfile
import os

groups = ["HC", "RBD", "PN", "MSA"]

fonace_a_lens = {}
fonace_i_lens = {}
monolog_lens = {}
zahradnik_lens = {}

for group in groups:

    fonace_a_lens[group] = []
    fonace_i_lens[group] = []
    monolog_lens[group] = []
    zahradnik_lens[group] = []

    fonace_path = Path(group)/"prodlouzena_fonace"
    if fonace_path.exists():
        for file_path in fonace_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == ".wav":

                # print(file_path)
                sample_rate, data = wavfile.read(file_path)
                sample_name = file_path.stem

                signal_duration = len(data)/sample_rate

                if sample_name[-1] == "a" or sample_name[-2] == "a":
                    fonace_a_lens[group].append(signal_duration)
                
                elif sample_name[-1] == "i" or sample_name[-2] == "i":
                    fonace_i_lens[group].append(signal_duration)
                
                else:
                    print(f"problem with {sample_name}")


    monolog_path = Path(group)/"monolog"
    if monolog_path.exists():
        for file_path in monolog_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == ".wav":

                # print(file_path)
                try:
                    sample_rate, data = wavfile.read(file_path)
                except Exception:
                    continue

                signal_duration = len(data)/sample_rate
                monolog_lens[group].append(signal_duration)
    
    zahradnik_path = Path(group)/"zahradnik"
    if zahradnik_path.exists():
        for file_path in zahradnik_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == ".wav":

                # print(file_path)
                sample_rate, data = wavfile.read(file_path)

                signal_duration = len(data)/sample_rate
                zahradnik_lens[group].append(signal_duration)



for group in groups:
    print(f"---------------- {group} ----------------")
    print(f"#Fonace a: {len(fonace_a_lens[group])}")
    print(f"Mean fonace a length: {np.mean(fonace_a_lens[group])}")
    print(f"Stdev fonace a length: {np.std(fonace_a_lens[group])}")
    print()
    print(f"#Fonace i: {len(fonace_i_lens[group])}")
    print(f"Mean fonace i length: {np.mean(fonace_i_lens[group])}")
    print(f"Stdev fonace i length: {np.std(fonace_i_lens[group])}")
    print()
    print(f"#Monolog: {len(monolog_lens[group])}")
    print(f"Mean monolog length: {np.mean(monolog_lens[group])}")
    print(f"Stdev monolog length: {np.std(monolog_lens[group])}")
    print()
    print(f"#Zahradnik: {len(zahradnik_lens[group])}")
    print(f"Mean zahradnik length: {np.mean(zahradnik_lens[group])}")
    print(f"Stdev zahradnik length: {np.std(zahradnik_lens[group])}")
    print()

    
all_fonace_a_lens = []
for arr in fonace_a_lens.values():
    all_fonace_a_lens.extend(arr)

all_fonace_i_lens = []
for arr in fonace_i_lens.values():
    all_fonace_i_lens.extend(arr)

all_monolog_lens = []
for arr in monolog_lens.values():
    all_monolog_lens.extend(arr)

all_zahradnik_lens = []
for arr in zahradnik_lens.values():
    all_zahradnik_lens.extend(arr)
                

print("---------------- /a/ ----------------")
print(f"Mean /a/: {np.mean(all_fonace_a_lens)}")
print(f"Stdev /a/: {np.std(all_fonace_a_lens)}")
print()

print("---------------- /i/ ----------------")
print(f"Mean /i/: {np.mean(all_fonace_i_lens)}")
print(f"Stdev /i/: {np.std(all_fonace_i_lens)}")
print()

print("---------------- Monolog ----------------")
print(f"Mean monolog: {np.mean(all_monolog_lens)}")
print(f"Stdev monolog: {np.std(all_monolog_lens)}")
print()

print("---------------- Zahradnik ----------------")
print(f"Mean zahradnik: {np.mean(all_zahradnik_lens)}")
print(f"Stdev zahradnik: {np.std(all_zahradnik_lens)}")
print()
               
