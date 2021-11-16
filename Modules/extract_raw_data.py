# External Library Imports
import os
import pandas as pd

# Project Level Imports
from Modules import config


def getPhysiologicalData(filename, separator, header, columns):
    """
    :param filename: Data file name as found in the 'physiological' directory
    :param separator: Separation character used to distinguish between columns
    :param header: Header row of the data file, None if no header is used
    :param columns: 'all' to return all columns, ['DaqTime', 'ECG'] to specify
    :return: Returns a pandas dataframe containing the physiological data
    """
    # Get the subjects physiological data (Subject-1)
    datasetPath = config.configurations["datasetPath"]
    physFilePath = os.path.join(datasetPath, "physiological", filename)
    physDF = pd.read_csv(physFilePath, sep=separator, header=header)
    physDF.columns = ["DaqTime", "ECG", "BVP", "GSR", "RSP", "SKT", "emg_zygo", "emg_coru", "emg_trap"]

    # Convert Time from seconds to ms with 3 decimal rounding
    physDF["DaqTime"] = physDF["DaqTime"].apply(lambda x: x * 1000).round(decimals=3)

    # Convert ECG (usually measured in millivolts (sensor I/P range +-40 mV))
    # And convert volts to milliVolts (mV) with rounding to three decimal places
    physDF["ECG"] = physDF["ECG"].apply(lambda x: ((x - 2.8) / 50) * 1000).round(decimals=3)

    if columns == 'all':
        return physDF
    else:
        return physDF[columns]


def getAnnotationData(filename, separator, header):
    """
    :param filename: Data file name as found in the 'Annotation' directory
    :param separator: Separation character used to distinguish between columns
    :param header: Header row of the data file, None if no header is used
    :return: Returns a pandas dataframe containing the JsTime and X/Y annotation data
    """
    # Get the subjects physiological data (Subject-1)
    datasetPath = config.configurations["datasetPath"]
    annFilePath = os.path.join(datasetPath, "annotations", filename)
    annDF = pd.read_csv(annFilePath, sep=separator, header=header)
    annDF.columns = ["JsTime", "Valence", "Arousal"]

    # Convert seconds into milliseconds and round to three decimal places
    annDF["JsTime"] = annDF["JsTime"].apply(lambda x: x * 1000).round(decimals=3)

    # Convert Joystick values Arousal(x) and Valence(y) axis values to range [0.5 9.5]
    annDF["Valence"] = annDF["Valence"].apply(lambda x: 0.5 + 9 * (x + 26225) / 52450)
    annDF["Arousal"] = annDF["Arousal"].apply(lambda x: 0.5 + 9 * (x + 26225) / 52450)

    return annDF


