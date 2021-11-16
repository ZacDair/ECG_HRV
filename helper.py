# External Library Imports
import numpy as np
import pandas as pd
import os

# Project Level Imports
from Modules import ecg_noise_reduction, ecg_peak_detection, extract_raw_data


# Extract the ECG data
physDF = extract_raw_data.getPhysiologicalData("sub1_DAQ.txt", "\t", None, ['DaqTime', 'ECG'])

# Extract the annotation data
annDF = extract_raw_data.getAnnotationData("sub1_joystick.txt", "\t", None)

print(annDF["JsTime"].head(10))
print(physDF["DaqTime"].head(10))

y = -1
res = pd.DataFrame(columns=["DaqTime", "JsTime", "ECG", "Arousal", "Valence"])
diff = 0
for x in physDF.index:
    try:
        physData = physDF.loc[x]

        if diff <= 0:
            y += 1
            annData = annDF.loc[y]
            diff = round(np.abs(physData["DaqTime"] - annData["JsTime"]))

        res.loc[x] = [physData["DaqTime"], annData["JsTime"], physData["ECG"], annData["Arousal"], annData["Valence"]]
        print("Diff:", diff)
        print("Index", x, "of", len(physDF))
        diff -= 1
    except IndexError or KeyError as e:
        print("Indexing Error")

print(res)
res.to_csv(os.path.join("output", "mergedCSV.csv"))

