from datetime import date, datetime, timedelta

def convert_to_date(d):
    if isinstance(d, date):
        return d
    elif isinstance(d, str):
        return datetime.strptime(d, '%Y-%m-%d').date()
    elif isinstance(d, int):
        s = str(d)
        if len(s) != 8:
            raise ValueError('Date must be YYYYMMDD')
        return date(int(s[:4]), int(s[4:6]), int(s[6:]))
    
def get_dates(start, end):
    start = max(convert_to_date(start), date(2017, 6, 28))
    end = min(convert_to_date(end), (date.today() - timedelta(days=1)))
    delta = (end - start).days

    return [start + timedelta(days=d) for d in range(delta + 1)]
    