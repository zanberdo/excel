import os
import errno
import pandas as pd


class Main:
    # Note: Pandas can read from an S3 source directly
    SITE_ROW_START = 4
    SITE_ROW_END = 13
    SITE_COL_START = 1
    SITE_COL_END = 4

    def __init__(self, site_characteristics_source, project_code):
        if not os.path.exists(site_characteristics_source):
            raise IOError(errno.ENOENT, os.strerror(errno.ENOENT), site_characteristics_source)
        site_characteristics = pd.ExcelFile(site_characteristics_source)

        if project_code not in site_characteristics.sheet_names:
            print(f'{project_code} not found in {site_characteristics.sheet_names}')
            raise Exception(f'Missing sheet {project_code}')
        self.dataframe = site_characteristics.parse(sheet_name=project_code, header=None)

    def run(self):
        site_level_df = self.get_dataframe(self.SITE_ROW_START, self.SITE_ROW_END,
                                           self.SITE_COL_START, self.SITE_COL_END)
        # print(site_level_df.to_string())
        # print(len(site_level_df.columns))
        # for key, value in site_level_df.itertuples():
        #     print('========================================')
        #     print(f'key:   [{key}]')
        #     print(f'value: [{value}]')
        # for item in site_level_df.iteritems():
        #     print('========================================')
        #     print(f'item: [{item}]')
        for row in site_level_df.iterrows():
            print('=========== iterrows() ===================')
            print(f'row type: [{type(row)}]')
            print(f'row size: [{len(row)}]')
            print(f'row[0]:   [{row[0]}]')
            print('---------------------------------')
            print(f'row[1]:   [{row[1].to_string()}]')
            print('---------------------------------')
            print(f'row[1]:   [{row[1]}]')

    def get_dataframe(self, row_start, row_end, col_start, col_end):
        # dataframe = self.dataframe.loc[row_start:row_end][list(self.dataframe.columns[col_start:col_end])]
        dataframe = self.dataframe.iloc[row_start:row_end][list(self.dataframe.columns[col_start:col_end])]
        return dataframe


if __name__ == '__main__':
    main = Main("/Users/mark.zanfardino/Documents/SD-1359/global checklist for solar site onboarding sample.xlsx",
                'DH1')
    main.run()

'''
# df = pd(site_characteristics)

# Iterate over all rows
# for index, row in df.iterrows():
#    print(row)

# Iterate over all named row tuples
# for row in df.itertuples():
    # print(row.Index)
    # print(f"{row.index} {row}")

# site_level = df[list(df.columns[0:4])].loc[1:8, :]
# site_level = df.loc[1:8, :][list(df.columns[0:1]) + list(df.columns[3:4])]
# print(type(site_level))
# print(site_level.to_string())

# feeder = df.loc[10:14][list(df.columns[0:1]) + list(df.columns[3:9])]
feeder = df.loc[10:14][list(df.columns[3:9])]
# print(type(feeder))
print(feeder.loc[10:10])
print("====================================")
feeder.columns = ['Feeder 1', 'Feeder 2', 'Feeder 3', 'Feeder 4', 'Feeder 5', 'Feeder 6']
print(feeder.to_string())
print("====================================")
# print(feeder.pivot)

# feeder_df = feeder.pivot_table(index=[], columns=[1,6])
# print(feeder_df)

# for row in feeder.itertuples():
#     print(f"{type(row)}: {row[0:6]}")
#     # for data in row:
#     #     print(f"{data}")
#
# print("====================================")
# feeder_pivot = feeder.pivot(columns='Valentine Solar')
# for row in feeder_pivot:
#    print(f"{type(row)}: {row[0:6]}")
# feeder_transpose = feeder.transpose()
feeder_transpose = feeder.set_index([pd.Index([1,2,3,4,5])]).T
# feeder_transpose = feeder.reset_index().T
print(feeder_transpose)

print("====================================")
for row in feeder_transpose:
    print(row)
'''
