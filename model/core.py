from datetime import timedelta

import pandas as pd


def df_from_db_with_date_format_col(client_id, db_path, datetime_col='datetime'):
    df = pd.read_excel(db_path)
    df = df.loc[df['client_id'] == client_id]
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    if df.empty:
        print('client: {} has no data in {}'.format(client_id, db_path))

    return df


def preprocess_timeseries(df, column, frequency, aggregation_function):
    df = df[['datetime', column]]
    df.set_index('datetime', inplace=True)
    df = df.resample(frequency).apply(aggregation_function)
    df.interpolate(limit_area='inside', inplace=True)
    df.dropna(inplace=True)

    return df


def subset_df_for_last_n_days(df, last_n_days, datetime_col):
    most_recent_date = df[datetime_col].max()
    date_n_days_ago_from_recent = most_recent_date - timedelta(days=last_n_days)
    df = df.loc[df[datetime_col] >= date_n_days_ago_from_recent].copy()

    return df
