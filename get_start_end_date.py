import calendar as calendar
import datetime

def get_start_end_date(year, month):
    """This function returns the first day and the last day, of a month, in string format.
    Date is returned in english format (yyyy-mm-dd)
    Input values:
    - year: string
    - month: string from 1 to 12

    Output values:
    - start_date: str in yyyy-mm-dd format
    - end_date: str in yyyy-mm-dd format
    """

    try:
        datetime.datetime(int(year), 10, 30)
    except ValueError:
        raise("Year variable has something wrong. Please check it")

    try:
        print(f"Ecco qui {month[0]}")
        if (int(month) < 10) and (int(month[0]) != 0):
            month = "0" + month
        datetime.datetime(2000, int(month), 30)
    except ValueError:
        raise("Month variable has something wrong. Please check it")

    start_date = year + "-" + month + "-" + str('01')
    end_date = year + "-" + month + "-" + str(calendar.monthrange(int(year),int(month))[1])

    return start_date, end_date

