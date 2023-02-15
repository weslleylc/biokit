import neurokit2 as nk

def get_rr_intervals(ecg_cleaned, **kwargs):
    """return the list of rr intervals.
    Args:
        ecg_cleaned: Cleaned ecg signal.
        sampling_rate: The sampling rate of the signal.
    Returns:
        Array with rr intervals in milliseconds
    """
    # R-peaks
    # 'pamtompkins1985', 'hamilton2002', 'christov2004', 'gamboa2008',
    # 'elgendi2010', 'engzeemod2012' ,'kalidas2017'
    if "method" not in kwargs:
        kwargs["method"] = "kalidas2017"
    if "correct_artifacts" not in kwargs:
        kwargs["correct_artifacts"] = True
    if "sampling_rate" not in kwargs:
        kwargs["sampling_rate"] = 128

    processed_data, rpeaks, = nk.ecg_peaks(
        ecg_cleaned=ecg_cleaned, **kwargs
    )

    rr_intervals_list = rpeaks["ECG_R_Peaks"][1:] - rpeaks["ECG_R_Peaks"][:-1]
    # convert to milliseconds
    rr_intervals_list *= (1000 / kwargs["sampling_rate"])
    return


def get_nn_intervals(rr_intervals, sampling_rate, **kwargs):
    """return the list of nn intervals.
    Args:
        rr_intervals: List of rr intervals.
        sampling_rate: The sampling rate of the signal.
    Returns:
        Array with nn intervals
    """
    pass


