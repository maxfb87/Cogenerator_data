import pandas as pd
import numpy as np

class MonthData():

    data = {}

    def __init__(self, year, month, start_date, end_date):
        self.data = {
        "month" : month,
        "year" : year,
        "start_date" : start_date,
        "end_date" : end_date,
        "is_loaded" : False,
    }

    def load_data(self):
        df_data = pd.read_excel("DATI.xlsx", sheet_name="DATI")
        self.data["is_loaded"] = True

    

