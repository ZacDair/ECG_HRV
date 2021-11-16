import os
import pandas as pd
import matplotlib.pyplot as plt

datasetPath = "D:/Projects/case_dataset/data/raw"


# Get all files from a directory and subdirectories, or all files of a specified type (eg: ".txt")
# returns a list of file paths
def getAllFiles(rootSearchPath, specificExt):
    filePaths = []
    # Search dirs and subdirs
    for root, dirs, files in os.walk(rootSearchPath):
        for file in files:
            if specificExt == "" or file.endswith(specificExt):
                filePath = os.path.join(root, file)
                filePaths.append(filePath)
                # Do file reading operations here

    print("Found", len(filePaths), "files in", rootSearchPath)
    return filePaths


# Get the subjects physiological data (Subject-1)
physFilePath = os.path.join(datasetPath, "physiological", "sub1_DAQ.txt")
physDF = pd.read_csv(physFilePath, sep="\t", header=None)
physDF.columns = ["DaqTime", "ECG", "BVP", "GSR", "RSP", "SKT", "emg_zygo", "emg_coru", "emg_trap"]
physDF = physDF[["DaqTime", "ECG"]]

# Get the subjects annotation data (Subject-1)
annFilePath = os.path.join(datasetPath, "annotations", "sub1_joystick.txt")
annDF = pd.read_csv(annFilePath, sep="\t", header=None)
annDF.columns = ["JsTime", "Valence", "Arousal"]

# Convert Time from seconds to ms with 3 decimal rounding
physDF["DaqTime"] = physDF["DaqTime"].apply(lambda x: x*1000).round(decimals=3)
annDF["JsTime"] = annDF["JsTime"].apply(lambda x: x*1000).round(decimals=3)

# Convert ECG (usually measured in millivolts (sensor I/P range +-40 mV))
# And convert volts to milliVolts (mV) with rounding to three decimal places
physDF["ECG"] = physDF["ECG"].apply(lambda x: ((x-2.8)/50)*1000).round(decimals=3)

# Convert Joystick values Arousal(x) and Valence(y) axis values to range [0.5 9.5]
annDF["Valence"] = annDF["Valence"].apply(lambda x: 0.5 + 9 * (x + 26225) / 52450)
annDF["Arousal"] = annDF["Arousal"].apply(lambda x: 0.5 + 9 * (x + 26225) / 52450)

"""
Sampling intervals are 1ms for physiological data, and 50ms for annotation data
"""

# annDF = pd.concat([annDF]*50, axis=0)
# annDF = annDF.sort_values(by="JsTime", ignore_index=True)
# mergedDf = pd.concat([annDF, physDF], axis=1)
# mergedDf.to_csv(os.path.join(os.getcwd(), "output", "merged_sub1.csv"))

# Plotting ECG and Valence/Arousal graphs
tempDF = physDF.head(5000)
plt.plot(tempDF['DaqTime'], tempDF['ECG'])
plt.show()
exit()
tempDF = annDF.head(60)
plt.plot(tempDF['JsTime'], tempDF['Valence'], color='g')
plt.plot(tempDF['JsTime'], tempDF['Arousal'], color='r')
plt.show()