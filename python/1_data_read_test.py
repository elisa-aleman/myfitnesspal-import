from datetime import datetime
import pandas
from useful_methods.ProjectPaths import *

df = pandas.read_csv(make_data_path("Health_Records_-_Body_Mass_Measurements_test_data.csv"))
# <select name="type" id="type" class="select">
# <option selected="selected" value="1">Weight</option>
# <option value="xxxxxxxxx">BMI</option>
# <option value="xxxxxxxxx">Body Fat Percentage</option>
columns = df.columns.to_list()
columns = [column.split("(")[0].strip() for column in columns]
df.columns = columns
df["Date"] = pandas.to_datetime(df["Date"], format="%Y.%m.%d")

use_cols = columns[1:]
# ['Weight', 
# 'BMI', 
# 'Body Fat Percentage']

cur_column="Weight"
selected = df[["Date",cur_column]].dropna()
# cur_input = list(selected.to_records(index=False))

cur_column="Body Fat Percentage"
selected = df[["Date",cur_column]].dropna()
selected[cur_column] = selected[cur_column].map(lambda x: x.strip('%'))
# cur_input = list(selected.to_records(index=False))


df2 = pandas.read_csv(make_data_path("Health_Records_-_Body_lenght_measurements_test_data.csv"))


columns = df2.columns.to_list()
columns = [column.split("(")[0].strip() for column in columns]
df2.columns = columns
df2["Date"] = pandas.to_datetime(df2["Date"], format="%Y.%m.%d")

use_cols = columns[1:]
# ['Height', 
# 'Waist', 
# 'Hips', 
# 'Bust', 
# 'Underbust', 
# 'Neck circumference']

cur_column="Height"
selected = df[["Date",cur_column]].dropna()
# cur_input = list(selected.to_records(index=False))


##########
df = pandas.read_csv(make_data_path("Health_Records_-_Body_Mass_Measurements_test_data.csv"))
df2 = pandas.read_csv(make_data_path("Health_Records_-_Body_lenght_measurements_test_data.csv"))
df3 = df.merge(df2,how='outer')
df3.to_csv(make_data_path("test_data.csv"))


columns = df3.columns.to_list()
columns = [column.split("(")[0].strip() for column in columns]
df3.columns = columns
df3["Date"] = pandas.to_datetime(df3["Date"], format="%Y.%m.%d")
use_cols = columns[1:]
# ['Weight', 
# 'BMI', 
# 'Body Fat Percentage',
# 'Height', 
# 'Waist', 
# 'Hips', 
# 'Bust', 
# 'Underbust', 
# 'Neck circumference']


cur_column="Height"
selected = df3[["Date",cur_column]].dropna()
for row in selected.itertuples():
	date = row[1]
	amount=row[2]
	print(date.year)
	print(amount)
