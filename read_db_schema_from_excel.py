import pandas as pd

db_file = './data/question_database_schema.xlsx'
dict_of_dfs = pd.read_excel(db_file, sheet_name = None)

for key in dict_of_dfs.keys():
    print(key)
    print(type(dict_of_dfs[key]))
    print(dict_of_dfs[key])