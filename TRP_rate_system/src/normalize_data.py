import pandas as pd
import numpy as np
from pathlib import Path
import openpyxl
from dataclasses import dataclass,field
'''
    TASK: block if __name__ == __main__
'''



# docs_folder = Path(Path.cwd()/'docs')
# data_upload = Path(docs_folder/ 'Выгрузка.xlsx')
# data_plan = Path(docs_folder/ 'План.xlsx')
# df_upload_raw = pd.read_excel(data_upload)

@dataclass
class UploadData:
    _path_excel_data:Path

    def normalize_upload_df(self):
        data_upload = self._path_excel_data
        df_upload_raw = pd.read_excel(data_upload,date_format=['Дата'])
        df_upload_raw['Время начала (5-29)'] = pd.to_datetime(df_upload_raw['Время начала (5-29)'], format="%H:%M:%S").dt.time
        df_upload_raw = df_upload_raw.rename(columns={
            'Ролик ID выхода'               :'ID_release',
            'Дата'                          :'date',
            'Время начала (5-29)'           :'time_begin',
            'Блок Распространение'          :'distribution_ch',
            'Ролик Тип'                     :'promo_video',
            "Ролик Ожидаемая длительность"  :'p_vid_duration',
            'Ролик Тип позиции в блоке'     :'p_vid_position',
            "Ролик ID"                      :'p_vid_ID',
            'Телекомпания'                  :'telecomp',
            "TVR All 25-55"                 :'TVR'

        })
        df_upload_raw[['p_vid_duration','TVR']] = df_upload_raw[['p_vid_duration','TVR']].apply(pd.to_numeric)
        df_upload_raw['month'] = df_upload_raw.date.dt.month
        return df_upload_raw

# df_upload= normalize_upload_df(df_upload_raw)


@dataclass
class PlanFactData():
    _path_excel_data:   Path
    df_plan         :   pd.DataFrame = field(repr=False,init=False)
    df_fact         :   pd.DataFrame = field(repr=False,init=False)
    def split_plan_fact_df(self):

        df_data_plan = pd.read_excel(self._path_excel_data)
        b_ind = df_data_plan.columns.get_loc('Бюджет')
        trp_ind = df_data_plan.columns.get_loc('TRP')-1
        bud = ['Бюджет' for i in range(trp_ind-b_ind+1)]
        trp = ['TRP' for i in range(trp_ind-b_ind+1)]
        df_data_plan.columns = df_data_plan.iloc[0,:]
        df_data_plan = df_data_plan.drop(0,axis=0)

        df_data_plan = df_data_plan.rename(columns={'Телеканал':'telecomp'})
        df_data_plan.index=df_data_plan.telecomp
        new = df_data_plan.drop(columns='telecomp').T

        new_1 = new.rename(columns={0:"month"})
        new_1 = new_1.apply(pd.to_numeric)

        df_plan, df_fact = np.split(new_1, 2)
        self.df_plan    = df_plan.T
        self.df_fact  = df_fact.T
        return self.df_plan,self.df_fact
@dataclass
class PlanFactTools:
    df:pd.DataFrame
    df_processed: pd.DataFrame = field(repr=False,init=False)
    def mapping_to_numeric_date(self):
        df_ = self.df
        month_rus   = ['Январь'	,'Февраль',	'Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
        month_numb  = list(range(1,13))

        df_ = df_.rename(columns=dict(zip(month_rus,month_numb))).reset_index()
        df_ = df_.rename(columns={'Телеканал':'telecomp'})
        self.df_processed = df_
        return self
    def melted_data(self):
        df_ = self.df_processed
        melted_df1 = pd.melt(df_, id_vars='telecomp', var_name='month', value_name='plan')


        melted_df1['telecomp'] = melted_df1['telecomp'].str.upper()

        melted_df1 = melted_df1.query('month !="Все месяцы"')
        self.df_processed = melted_df1
        return self


if __name__ == '__main__':
    docs_folder = Path(Path.cwd()/'TRP_rate_system'/'src'/'docs')

    data_upload = Path(docs_folder/ 'Выгрузка.xlsx')
    data_plan = Path(docs_folder/ 'План.xlsx')


    upload_data = UploadData(_path_excel_data=data_upload)
    df_upload = upload_data.normalize_upload_df()

    plan_fact = PlanFactData(_path_excel_data=data_plan)

    df_audience,df_tvr =  plan_fact.split_plan_fact_df()

    df_audience_prdessed = PlanFactTools(df_audience) \
        .mapping_to_numeric_date() \
        .melted_data() \
        .df_processed

    df_tvr_prdessed = PlanFactTools(df_tvr) \
        .mapping_to_numeric_date() \
        .melted_data() \
        .df_processed
    print(df_tvr_prdessed)


# df_data_plan_raw = pd.read_excel(data_plan)

# df_budget_raw,df_trp_raw= normalize_plan_fact_df(df_data_plan=df_data_plan_raw)

# df_budget = mapping_to_numeric_date(df_budget_raw)
# df_trp = mapping_to_numeric_date(df_trp_raw)