import numpy as np
import pandas as pd


def read_csv(filename):
    names ='date sdate payee account currency amount flag memo'.split()
    df = pd.read_csv(filename, names=names, na_filter=False)
    df['date_t'] = pd.to_datetime(df['date'])
    df = df.sort_values(['date', 'amount'], ascending=[True, False])
    return df

def df_jpy(df):
    return df.loc[df['currency'] == '']

def df_currency(df, currency=''):
    return df.loc[df['currency'] == currency]

def grid_data(df, year):
    df_y = df_jpy(df)
    df_y = df_y.loc[df_y['date_t'].dt.year == year]
    df_p = pd.pivot_table(df_y,
                          values='amount',
                          index='account',
                          columns=df['date_t'].dt.month,
                          aggfunc=np.sum,
                          fill_value=0).reset_index()
    df_p['sum'] = df_p.sum(axis=1)

    return df_p.rename(columns={k: f'm{k:02}' for k in range(1,13)})

def grid_years(df):
    df_y = df_jpy(df)
#    df_y = df_y.loc[df_y['payee'] == 'amazon']
    df_y = df_y.loc[(df['date_t'].dt.year >= 2016) & (df['date_t'].dt.year <= 2021)]
    df_p = pd.pivot_table(df_y,
                          values='amount',
                          index='account',
                          columns=df['date_t'].dt.year,
                          aggfunc=np.sum,
                          fill_value=0).reset_index()
    df_p['sum'] = df_p.sum(axis=1)

    columns = {t: f'y{t:04}' for t in df_p.columns if isinstance(t, int)}
    return df_p.rename(columns=columns)

def grid_payee(df, account):
    df_jp = df_jpy(df)
    df_jp = df_jp.loc[(df_jp['date_t'].dt.year >= 2016) & (df_jp['date_t'].dt.year <= 2021)]
    df_acct = df_jp.loc[df_jp['account'] == account]
    df_grid = pd.pivot_table(df_acct,
                             values='amount',
                             index='payee',
                             columns=df_acct['date_t'].dt.year,
                             aggfunc=np.sum,
                             fill_value=0).reset_index()
    df_grid['sum'] = df_grid.sum(axis=1)
    columns = {t: f'y{t:04}' for t in df_grid.columns if isinstance(t, int)}
    return df_grid.rename(columns=columns)


def read_accounts_csv(filename):
    names ='number name'.split()
    df = pd.read_csv(filename, names=names, na_filter=False)
    return df


def account_by_number(df, number):
    return df.loc[df['number'] == number]['name'].values[0]


def account_by_name(df, name):
    return df.loc[df['name'] == name]['number'].values[0]


def read_payees_csv(filename):
    names ='number name'.split()
    df = pd.read_csv(filename, names=names, na_filter=False)
    return df


def payee_by_number(df, number):
    return df.loc[df['number'] == number]['name'].values[0]
