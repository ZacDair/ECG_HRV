# External Library Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Project Level Imports
from Modules import ecg_noise_reduction, ecg_peak_detection, extract_raw_data

# Plot style settings
sns.set(style='whitegrid', rc={'axes.facecolor': '#EFF2F7'})

# Duration of signal to analyze (ms)
DURATION = 5000

# Extract the ECG data
physDF = extract_raw_data.getPhysiologicalData("sub1_DAQ.txt", "\t", None, ['DaqTime', 'ECG'])

# detect peaks
fs = 200  # corresponds to 60 beats per min (normal for human), assumed.
lowcut = 0.05 * 3.3  # 9.9 beats per min
highcut = 15  # 900 beats per min
y = ecg_noise_reduction.butter_bandpass_forward_backward_filter(physDF['ECG'], lowcut, highcut, fs, order=4)

reducedDf = pd.DataFrame(data=y.tolist(), columns=["reducedECG"])
physDF["ECG"] = reducedDf["reducedECG"]

if DURATION:
    peaks, similarity = ecg_peak_detection.detect_peaks(physDF.head(DURATION)["ECG"], threshold=0.6)
else:
    peaks, similarity = ecg_peak_detection.detect_peaks(physDF["ECG"], threshold=0.6)

# group peaks so we get a single peak per beat
grouped_peaks = ecg_peak_detection.group_peaks(peaks)

# RR-intervals are the differences between successive peaks
rr = np.diff(grouped_peaks)
print("RR Intervals:", rr)

hrv = []
for x in rr:
    if x > 80:
        hrv.append(x)

print("HRV:", hrv)
print("Mean HRV:", np.mean(hrv))
print("Min HRV:", min(hrv))
print("Max HRV:", max(hrv))
print("STD HRV:", np.std(hrv))

# Remap indexes to DaqTime/ECG values
peaks = physDF.loc[peaks]

# Plot 5000ms of ECG and Peaks
tempDF = physDF.head(DURATION)
plt.plot(tempDF['DaqTime'], tempDF['ECG'])
# plt.plot(peaks['DaqTime'], peaks['ECG'], markersize=5, label="peaks", color="orange", marker="o",linestyle="None")
plt.plot(peaks['DaqTime'], np.repeat(1, peaks.shape[0]), markersize=1, label="peaks", color="orange", marker="o", linestyle="None")
plt.plot(grouped_peaks, np.repeat(0.5, grouped_peaks.shape[0]), markersize=1, label="gpeaks", color="red", marker="o", linestyle="None")
plt.show()
