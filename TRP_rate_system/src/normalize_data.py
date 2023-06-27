import pandas as pd
import numpy as np
from pathlib import Path
import openpyxl

docs_folder = Path(Path.cwd()/'src'/'docs')

data_upload = Path(docs_folder/ 'Выгрузка.xlsx')
data_plan = Path(docs_folder/ 'План.xlsx')
# df_upload_raw = pd.read_excel(data_upload)

print(data_upload)

