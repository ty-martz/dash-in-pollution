import pickle
import pandas as pd

def load_correlation_dict(path='../data/outputs/corr_dict.pkl'):
    return pickle.load(open(path, 'rb'))

def load_correlation_df(path='../data/outputs/corr_dict.pkl'):
    df = pd.DataFrame(pickle.load(open(path, 'rb'))).transpose().reset_index()
    df.columns = ['City', 'CO', 'NO2', 'SO2', 'PM2.5', 'AQI']
    return df

def load_full_data_and_predictions(): # 11 million rows of data across 46 columns
    return pickle.load(open('../data/outputs/all_data_predictions.pkl', 'rb'))

def load_monthly_with_unemployment(path='data/monthly_gas_econ.pkl'):
    df =  pickle.load(open(path, 'rb'))
    df['date'] = pd.to_datetime(df['fiscalno'].astype(str) + '01', format='%Y%m%d').dt.strftime('%m/%d/%Y')
    #df['date'] = datetime.datetime(df['fiscalno'].astype(str).str[:4].astype(int), df['fiscalno'].astype(str).str[-2:].astype(int), 1).strftime('%m/%d/%Y')
    df['year'] = df['fiscalno'].astype(str).str[:4].astype(int)
    df.columns = ['city', 'fiscalno', 'co', 'no2', 'so2', 'pm2.5', 'unemployment', 'aqi', 'date', 'year']
    return df

def load_change_monthly_with_unemployment(path='data/monthly_gas_econ.pkl'):
    #df = pickle.load(open(path, 'rb'))
    df = pd.read_pickle(path)
    df['unemployment_change'] = df['est_unemployment_pct'].diff()
    for g in ['co_api', 'no2_api', 'so2_api', 'pm2.5_api', 'aqi']:
        df[f'diff_{g}'] = df[g].pct_change()

    return df

def load_quarterly_change_with_unemployment(): # to be used in 2x2 matrix
    q_mapping = {
        '01':'Q1', '02':'Q1', '03':'Q1',
        '04':'Q2', '05':'Q2', '06':'Q2',
        '07':'Q3', '08':'Q3', '09':'Q3',
        '10':'Q4', '11':'Q4', '12':'Q4',
    }
    ddf = load_change_monthly_with_unemployment()
    ddf['quarter_string'] = ddf['fiscalno'].astype(str).str[-2:].map(q_mapping) + '-' + ddf['fiscalno'].astype(str).str[:4]
    ddf['quarter'] = ddf['fiscalno'].astype(str).str[-2:].map(q_mapping).str[-1:].astype(int)
    ddf['year'] = ddf['fiscalno'].astype(str).str[:4].astype(int)

    df = ddf.copy()
    grp = pd.DataFrame(df.groupby(
        ['city', 'year', 'quarter_string', 'quarter']
        )[['co_api', 'no2_api', 'so2_api', 'pm2.5_api', 'aqi', 'est_unemployment_pct']].mean()).reset_index()
    grp['unemployment_change'] = grp['est_unemployment_pct'].diff()
    for g in ['co_api', 'no2_api', 'so2_api', 'pm2.5_api', 'aqi']:
        grp[f'diff_{g}'] = grp[g].pct_change() * 100
    grp.drop(grp[grp['quarter_string'] == 'Q1-2018'].index, inplace=True)

    return grp

def load_regression_models_dict(path='../data/outputs/reg_dict.pkl'):
    return pickle.load(open(path, 'rb'))

def load_covid_cases(path='who_covid_in.csv'):
    cov = pd.read_csv(path)
    cov = cov[cov.Country == 'India']
    cov['Date_reported'] = pd.to_datetime(cov['Date_reported'])
    return cov

def load_grouped_covid_pollution(covid_path='data/who_covid_in.csv'):
    cov = load_covid_cases(covid_path)
    df = load_full_data_and_predictions()
    df = df[['date_int', 'city_id', 'co_api', 'so2_api', 'no2_api', 'pm2.5_api']]
    df['date'] = pd.to_datetime(df['date_int'], format='%Y%m%d')
    all = pd.merge(df, cov, 'left', right_on='Date_reported', left_on='date').dropna(axis=0).sort_values('date').reset_index(drop=True)

    grp = all.groupby(['date']).agg({'co_api':'mean', 'no2_api':'mean', 'so2_api':'mean', 'pm2.5_api':'mean', 'New_cases':'max'})
    grouped = pd.DataFrame(grp).reset_index()
    return grouped


def load_corr_reg_table(city='Agartala', corr=load_correlation_df, reg=load_regression_models_dict):
    # get city correlations
    corr = pickle.load(open('data/corr_df.pkl', 'rb'))
    df1 = corr.set_index('City')
    cit = df1[df1.index == city].transpose()
    # get regression model
    reg = pickle.load(open('data/reg_mods.pkl', 'rb'))
    dat = pd.DataFrame(reg[city].params).reset_index(drop=True).iloc[1:]
    dat.index = ['CO', 'NO2', 'SO2', 'PM2.5', 'AQI']
    # merge
    both = pd.merge(cit,dat,'left', left_index=True, right_index=True)
    for col in list(both.columns):
        both[col] = both[col].round(4)
    both = both.reset_index()
    both.columns = ['Gas', 'Correlation', 'Regression Coefficient']
    return both
