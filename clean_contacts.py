import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

def get_clean_contacts(contacts):

    #Selecting only names and phone numbers from contacts_main
    contacts_main = contacts[['First name', 'Last name', 'Phone : ', 'Phone : mobile', 'Phone : home', 'Phone : iPhone', 'Phone : other']].copy(deep=True)
    contacts_main.rename(columns={'First name': 'first_name',
                                'Last name': 'last_name',
                                'Phone : ': 'phone_1',
                                'Phone : mobile': 'phone_2',
                                'Phone : home': 'phone_3',
                                'Phone : iPhone': 'phone_4',
                                'Phone : other': 'phone_5'},
                                inplace=True)

    #Removing all spaces from phone numbers
    for i in range(contacts_main.shape[0]):
        if pd.isna(contacts_main.phone_1[i]):
            if not pd.isna(contacts_main.phone_2[i]):
                contacts_main.phone_1[i] = contacts_main.phone_2[i]
                contacts_main.phone_2[i] = np.nan
            elif not pd.isna(contacts_main.phone_3[i]):
                contacts_main.phone_1[i] = contacts_main.phone_3[i]
                contacts_main.phone_3[i] = np.nan
            elif not pd.isna(contacts_main.phone_4[i]):
                contacts_main.phone_1[i] = contacts_main.phone_4[i]
                contacts_main.phone_4[i] = np.nan
            elif not pd.isna(contacts_main.phone_5[i]):
                contacts_main.phone_1[i] = contacts_main.phone_5[i]
                contacts_main.phone_5[i] = np.nan
                
    for i in range(contacts_main.shape[0]):
        if pd.isna(contacts_main.phone_2[i]):
            if not pd.isna(contacts_main.phone_3[i]):
                contacts_main.phone_2[i] = contacts_main.phone_3[i]
                contacts_main.phone_3[i] = np.nan
            elif not pd.isna(contacts_main.phone_4[i]):
                contacts_main.phone_2[i] = contacts_main.phone_4[i]
                contacts_main.phone_4[i] = np.nan
            elif not pd.isna(contacts_main.phone_5[i]):
                contacts_main.phone_2[i] = contacts_main.phone_5[i]
                contacts_main.phone_5[i] = np.nan

    #Removing empty columns
    contacts_main.drop(['phone_3', 'phone_4', 'phone_5'], axis=1, inplace=True)

    #Creating new df for TSZ residents
    contacts_tsz = pd.DataFrame()

    #Adding only TSZ residents to the contacts_tsz dataframe
    for i in range(contacts_main.shape[0]):
        if '🏡' in str(contacts_main['first_name'][i]):
            contacts_tsz = pd.concat([contacts_tsz, contacts_main.iloc[[i]]])
            
    for i in range(contacts_main.shape[0]):
        if str(contacts_main['first_name'][i]).isdigit():
            contacts_tsz = pd.concat([contacts_tsz, contacts_main.iloc[[i]]])

    #Removing unnecessary symbols from the first names of TSZ residents
    contacts_tsz['first_name'] = contacts_tsz['first_name'].str.replace('🏡', '').str.lstrip()

    # Replace missing values in 'last_name' with an empty string
    contacts_tsz['last_name'].fillna('', inplace=True)

    #Adding apartment number column to the contacts_tsz dataframe
    contacts_tsz['apartment_number'] = np.nan

    condition_kv = contacts_tsz['last_name'].str.contains('кв')
    condition_kv_qu = contacts_tsz['last_name'].str.contains('\?\?\?')

    contacts_tsz.loc[condition_kv, 'apartment_number'] = contacts_tsz.loc[condition_kv, 'last_name'].str.split().str[-1]
    contacts_tsz.loc[condition_kv, 'last_name'] = contacts_tsz.loc[condition_kv, 'last_name'].str.split().str[0]
    contacts_tsz.loc[condition_kv_qu, 'last_name'] = np.nan
    contacts_tsz['last_name'] = contacts_tsz['last_name'].str.replace('кв', '').str.lstrip()

    #Adding apartment number column to the contacts_tsz dataframe rows without names
    condition_noname = contacts_tsz['first_name'].str.isdigit()
    contacts_tsz.loc[condition_noname, 'apartment_number'] = contacts_tsz.loc[condition_noname, 'first_name']
    contacts_tsz.loc[condition_noname, ['first_name', 'last_name']] = np.nan

    #Changing phone numbers to +7
    contacts_tsz['phone_1'] = contacts_tsz['phone_1'].str.replace('8 ', '+7 ')

    #Inserting NaN into empty last_names
    contition_emty_last_name = contacts_tsz['last_name'] == ''
    contacts_tsz.loc[contition_emty_last_name, 'last_name'] = np.nan

    #cast apartment numbers to int
    condition_not_nan = contacts_tsz['apartment_number'] == np.nan
    contacts_tsz['apartment_number'] = contacts_tsz['apartment_number'].fillna(0)
    contacts_tsz['apartment_number'] = contacts_tsz['apartment_number'].astype('int16')
    return contacts_tsz