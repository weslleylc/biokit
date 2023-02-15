from typing import Dict

import neurokit2 as nk
import numpy as np
import tsfel
from neurokit2.ecg.ecg_quality import (
    _ecg_quality_basSQI,
    _ecg_quality_kSQI,
    _ecg_quality_pSQI,
)
from scipy.signal import find_peaks


def compute_zhao(
    ecg_cleaned: str,
    sampling_rate: int,
    first_method: str = "pantompkins1985",
    second_method: str = "kalidas2017",
    **kwargs
) -> Dict[str, float]:
    # Compute indexes
    kSQI = _ecg_quality_kSQI(ecg_cleaned)
    pSQI = _ecg_quality_pSQI(ecg_cleaned, sampling_rate=sampling_rate)
    basSQI = _ecg_quality_basSQI(ecg_cleaned, sampling_rate=sampling_rate)

    # Extract R-peaks locations
    _, rpeaks = nk.ecg_peaks(
        ecg_cleaned, sampling_rate=sampling_rate, method=first_method
    )
    rpeaks = rpeaks["ECG_R_Peaks"]

    # Extract R-peaks locations
    _, rpeaks_cwt = nk.ecg_peaks(
        ecg_cleaned, sampling_rate=sampling_rate, method=second_method
    )
    rpeaks_cwt = rpeaks_cwt["ECG_R_Peaks"]

    if len(rpeaks) > 0 and len(rpeaks_cwt):
        qSQI = (
            2
            * len(set(rpeaks_cwt).intersection(set(rpeaks)))
            / (len(rpeaks_cwt) + len(rpeaks))
        )
    else:
        qSQI = 0.0

    return {"kSQI": kSQI, "pSQI": pSQI, "basSQI": basSQI, "qSQI": qSQI}


def compute_rodrigues(
    ecg_cleaned: np.ndarray, signal_duration: float = 10.0
) -> Dict[str, float]:
    # STD - Standard Deviation
    std = tsfel.calc_std(ecg_cleaned)
    # ZCR - Zero Crossing Rate
    zcr = tsfel.zero_cross(ecg_cleaned)

    # PD - Peaks Distance
    sample_smooth = nk.signal_smooth(ecg_cleaned, kernel="blackman")
    stdsmooth = tsfel.calc_std(sample_smooth)
    peaksabovestd, _ = find_peaks(sample_smooth, height=stdsmooth)
    if len(peaksabovestd) == 0:
        return {"STD": std, "PR": 0, "PD": 0, "AD": 0, "ZCR": zcr}
    peaksdistance = 0.0
    for i in range(1, len(peaksabovestd)):
        peaksdistance += peaksabovestd[i] - peaksabovestd[i - 1]
    peaksdistance *= signal_duration / (len(ecg_cleaned) * len(peaksabovestd))

    # PR - Peaks Rate
    peaksrate = nk.signal_rate(peaksabovestd)
    # peaksrate = len(peaksabovestd)

    # AD - Amplitude Difference
    troughsbelowstd, _ = find_peaks(-sample_smooth, height=stdsmooth)
    sum_max = sum(ecg_cleaned[peaksabovestd])
    sum_min = sum(ecg_cleaned[troughsbelowstd])
    ad = sum_max - sum_min

    return {
        "STD": std,
        "PR": np.mean(peaksrate),
        "PD": peaksdistance,
        "AD": ad,
        "ZCR": zcr,
    }
