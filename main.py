from get_cogen_saving import *
from get_best_regime import *
from get_start_end_date import *
from join_txt_files import *
import cogendata


print('START MAIN')
#year = input('Please type the year ')
#month = input('Please type the month ')

year = str(2022) #just for test without insert every time these variables
month = str(1) #just for test without insert every time these variables


start_date, end_date = get_start_end_date(year, month)

february22 = cogendata.MonthData(year, month, start_date, end_date)

february22.load_data()






# saving = get_cogen_saving(0.5, 100, 100, ["-ekc"])
# #print("---------")
# #print(f"SAVING: {str(saving)}")
# best_regime = get_best_regime(132, 300, ["-verbose"])

# print(f"BEST REGIME: {best_regime}")

#start_date, end_date = get_start_end_date("2020", "05")

#join_txt_files()


