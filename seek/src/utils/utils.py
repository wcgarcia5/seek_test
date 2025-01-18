from datetime import datetime, date


@staticmethod
def convert_dates(data):
    """
        Converts date objects to datetime objects within a dictionary.
        Args:
            data: The dictionary containing potential date objects.

        Returns:
            A new dictionary with all `date` objects converted to `datetime` objects.
    """
    for key, value in data.items():
        if isinstance(value, (date, datetime)):  # Detecta tipo date y datetime
            if isinstance(value, date):
                data[key] = datetime.combine(value, datetime.min.time())
    return data
