import pandas as pd
import os

leads_path = os.path.join("Input_data","leads_links.xlsx")

def  links_leads(platform):
    df = pd.read_excel(leads_path)

    df = df[df['Platform'] == platform]

    def short_name(x):
        try:
            x = x.split('-')[1]
            return x
        except:
            return x
    df['short_name'] = df['Account Name (Seller Name) (Account)'].apply(short_name)
    
    list_lead_short_name = df['short_name'].tolist()

    list_lead_real_name = df['Account Name (Seller Name) (Account)'].tolist()

    list_source_campaign = df['Source_campaign'].tolist()

    list_country = df['Country'].tolist()

    list_profile_url = df['Profile_link'].tolist()

    return list_lead_short_name, list_lead_real_name, list_source_campaign, list_country, list_profile_url