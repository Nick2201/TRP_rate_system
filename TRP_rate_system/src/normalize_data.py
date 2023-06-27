import pandas as pd
import numpy as np
from pathlib import Path
import openpyxl
'''
    TASK: block if __name__ == __main__
'''
# docs_folder = Path(Path.cwd()/'TRP_rate_system'/'src'/'docs')

# data_upload = Path(docs_folder/ 'Выгрузка.xlsx')
# data_plan = Path(docs_folder/ 'План.xlsx')
# df_upload_raw = pd.read_excel(data_upload)


docs_folder = Path(Path.cwd()/'docs')
data_upload = Path(docs_folder/ 'Выгрузка.xlsx')
data_plan = Path(docs_folder/ 'План.xlsx')
df_upload_raw = pd.read_excel(data_upload)



def normalize_upload_df(df_upload_raw):
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

df_upload= normalize_upload_df(df_upload_raw)

def normalize_plan_fact_df(df_data_plan):

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



    df_plan, df_result = np.split(new_1, 2)
    return df_plan.T,df_result.T

def mapping_to_numeric_date(df_):
    month_rus   = ['Январь'	,'Февраль',	'Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
    month_numb  = list(range(1,13))

    df_ = df_.rename(columns=dict(zip(month_rus,month_numb))).reset_index()
    df_ = df_.rename(columns={'Телеканал':'telecomp'})
    return df_


df_data_plan_raw = pd.read_excel(data_plan)

df_budget_raw,df_trp_raw= normalize_plan_fact_df(df_data_plan=df_data_plan_raw)

df_budget = mapping_to_numeric_date(df_budget_raw)
df_trp = mapping_to_numeric_date(df_trp_raw)