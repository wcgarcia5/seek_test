from datetime import datetime, date
from typing import Union, List, Dict


@staticmethod
def convert_dates(data: Union[Dict, List[Dict]]) -> Union[Dict, List[Dict]]:
    """
    Converts date objects to datetime objects within a dictionary or a list of dictionaries.

    Args:
        data: The input data, either a dictionary or a list of dictionaries, containing potential date objects.

    Returns:
        The input data with all `date` objects converted to `datetime` objects for mongoDB
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (date, datetime)):
                if isinstance(value, date):
                    data[key] = datetime.combine(value, datetime.min.time())
        return data

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, (date, datetime)):
                        if isinstance(value, date):
                            item[key] = datetime.combine(value, datetime.min.time())
        return data
