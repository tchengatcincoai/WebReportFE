import datetime


def epoch_to_datetime(epoch_timestamp, datetime_format):
    """
    convert epoch time with milliseconds to datetime string format
    :param epoch_timestamp: float, lowest digit stands for seconds
    :param datetime_format: string
    :return: string of datetime
    """
    return datetime.datetime.fromtimestamp(epoch_timestamp).strftime(datetime_format)