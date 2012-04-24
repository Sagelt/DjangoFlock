from datetime import datetime, timedelta

def datetime_range(start, end, step=timedelta(hours=1)):
    """
    Generator for a list of datetimes. If step is not provided, defaults to one
    hour increments.
    
    Behaves much like range, except the end is inclusive.
    """
    if not isinstance(start, datetime):
        raise ValueError("start must be a datetime.")
    if not isinstance(end, datetime):
        raise ValueError("end must be a datetime.")
    if not isinstance(step, timedelta):
        raise ValueError("step must be a timedelta.")
    current = start
    while current <= end:
        yield current, current + step
        current += step
