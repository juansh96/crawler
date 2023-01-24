import os
import pandas as pd

from helper_functions_main import rename_platforms

# read the input file

input_path = os.path.join('Input_data','leads_links.xlsx')
df = pd.read_excel(input_path)

df['Platform'] = df['Platform'].apply(rename_platforms)

#filter df by platform

list_of_platforms = df['Platform'].unique().tolist()

for platform in list_of_platforms:
    df_platform = df[df['Platform'] == platform]
    
    try:    
        crawler_path = os.path.join('platforms',str(platform).lower(),'main.py')
        print('crawler_path: ', crawler_path)
        exec(open(crawler_path).read())
    
    except Exception as e:
        print(e)
        print('No se pudo ejecutar el crawler de la plataforma: ', platform)


    

