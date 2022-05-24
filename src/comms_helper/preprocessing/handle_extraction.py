HANDLE_REG = "@\w{1,15}"


def extract_handles(ser):
    """

    Parameters
    ----------
    ser : pd.Series
        note: choose useful index for this series

    Returns
    -------
    pd.Series
        explanded series with all mentions extracted
    """
    return ser.str.findall(HANDLE_REG).explode().dropna().str.lstrip("@")

