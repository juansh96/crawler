import os
import pandas as pd
from datetime import datetime

from helper_functions_main import rename_platforms, concat_ads, concat_errors_platform, concat_errors_leads

# read the input file

input_path = os.path.join('Input_data','leads_links.xlsx')
output_path_platform_errors = os.path.join('Output_data','Errors','Platform',f'platform_errors_{datetime.now()}.xlsx')

df = pd.read_excel(input_path)

df['Platform'] = df['Platform'].apply(rename_platforms)

#filter df by platform

list_of_platforms = df['Platform'].unique().tolist()
errors_list = []

for platform in list_of_platforms:
    df_platform = df[df['Platform'] == platform]
    
    try:    
        crawler_path = os.path.join('platforms',str(platform).lower(),'main.py')
        print('crawler_path: ', crawler_path)
        exec(open(crawler_path).read())
    
    except Exception as e:
        print(e)
        print('No se pudo ejecutar el crawler de la plataforma: ', platform)
        errors_list.append({'Platform': platform, 'Error': e})

# save the output errors file

try:
    df_errors = pd.DataFrame(errors_list)
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H-%M-%S")
    output_path_platform_errors = os.path.join('Output_data','Errors','Platform',f'platform_errors_{now}.xlsx')
    df_errors.to_excel(output_path_platform_errors, index=False)
except Exception as e:
    print(e)

# concat all the files
concat_ads()
concat_errors_platform()
concat_errors_leads()





    

