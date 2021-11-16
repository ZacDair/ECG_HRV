# # External Library Imports
# import numpy as np
# import pandas as pd
# import os
#
# # Project Level Imports
# from Modules import ecg_noise_reduction, ecg_peak_detection, extract_raw_data
#
#
# # Extract the ECG data
# physDF = extract_raw_data.getPhysiologicalData("sub1_DAQ.txt", "\t", None, ['DaqTime', 'ECG'])
#
# # Extract the annotation data
# annDF = extract_raw_data.getAnnotationData("sub1_joystick.txt", "\t", None)
#
# # Loop through for each 50 DaqTime, take JsTime
# # i = 0
# # y = 0
# # for x in physDF['DaqTime']:
# #     try:
# #         print("DaqTime: ", x, "JsTime:", annDF.iloc[y]['JsTime'])
# #         print("Similar:", np.isclose(x, annDF.iloc[y]['JsTime']))
# #     except KeyError or IndexError as e:
# #         print("Missing Index:", x)
# #
# #     jsTime = annDF.iloc[y]['JsTime']
# #     print("DaqTime: ", x, "JsTime:", jsTime)
# #     print("i:", i, "y:", y)
# #     if i % 50 == 0:
# #         y += 1
# #     i += 1
#
# # Get every 50th row
# # shorterDF = physDF.iloc[::50]
# res = pd.DataFrame(columns=["DaqTime", "JsTime", "ECG", "Arousal", "Valence"])
# diff = 0
# row = -1
# for x in physDF.index:
#     physData = physDF.loc[x]
#     print("Index", x, "of", len(physDF))
#     print("Diff:", diff)
#     if diff > 0:
#         res.loc[x] = [physData["DaqTime"], row["JsTime"], physData["ECG"], row["Arousal"], row["Valence"]]
#     else:
#         if len(annDF) > 1:
#             row = annDF.iloc[0]
#             nextRow = annDF.iloc[1]
#             diff = nextRow["JsTime"] - row["JsTime"]
#         else:
#             prev = row
#             row = annDF.iloc[0]
#             diff = row["JsTime"] - prev["JsTime"]
#
#         res.loc[x] = [physData["DaqTime"], row["JsTime"], physData["ECG"], row["Arousal"], row["Valence"]]
#         annDF = annDF.drop(0).reset_index(drop=True)
#         print(annDF)
#
#     if len(annDF) == 0:
#         break
#     diff -= 1
#
# print(res)
# res.to_csv(os.path.join("output", "mergedCSV.csv"))

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

res = pd.DataFrame(columns=["DaqTime", "JsTime", "ECG", "Arousal", "Valence"])
times = annDF['JsTime']
for x in annDF.index:
    annRow = annDF.loc[x, 'JsTime']
    nearPhysRows = physDF[(annDF.loc[x]['JsTime'] - 500 <= physDF['DaqTime']) & (physDF['DaqTime'] <= annDF.loc[x]['JsTime'] + 500)]
    nearPhysRows = nearPhysRows.loc[:].copy()
    nearPhysRows["JsTime"] = annDF.loc[x]['JsTime']
    nearPhysRows["Arousal"] = annDF.loc[x]['Arousal']
    nearPhysRows["Valence"] = annDF.loc[x]['Valence']
    res = res.append(nearPhysRows)
    print(x, "of", len(annDF))

res.to_csv(os.path.join("output", "mergedCSV-500ms.csv"))

# Possible faster solution
# physDF where daqtime_current_row <= jsTime <= daqTime_next_row
# find daqtime value or +- (10 ms) rounded up in jsTime values, copy over the annotations

# Possibe alt solution
# split physDF into n segments, if segments row 1 daqtime <= jsTime <= daqTime
# copy over annotations else omitt where no annotations were found


