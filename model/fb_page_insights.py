from datetime import timedelta

from core import subset_df_for_last_n_days
from fb_list_of_posts import get_df_fb_list_of_posts
from model.core import preprocess_timeseries, df_from_db_with_date_format_col


def get_df_fb_page_insights(client_id):
    db_path_from_root = '/Users/abhilash/Insofe/Projects/socialight/app/insights_app/model/database/1_fb_page_insights.xlsx'
    df = df_from_db_with_date_format_col(client_id=client_id, db_path=db_path_from_root)

    return df


def get_lifetime_likes_meter_values(client_id):
    df = get_df_fb_page_insights(client_id=client_id)
    if df.empty:
        likes_recent = likes_month_ago = 0
        return likes_recent, likes_month_ago

    likes_recent, date_most_recent = get_lifetime_recent_likes_and_datetime(client_id, df)
    likes_month_ago = get_lifetime_likes_a_month_ago_from_recent_update(df, date_most_recent)
    likes_month_ago = 0 if likes_month_ago.empty else likes_month_ago.values[0]

    return likes_recent, likes_month_ago


def get_lifetime_likes_a_month_ago_from_recent_update(df, date_most_recent):
    days_in_a_month = 30
    date_month_ago = date_most_recent - timedelta(days=days_in_a_month)
    likes_month_ago = df.loc[df['datetime'] <= date_month_ago, 'lifetime_total_likes']

    return likes_month_ago


def get_lifetime_recent_likes_and_datetime(client_id, df):
    date_most_recent = df['datetime'].max()
    likes_recent = df.loc[df['datetime'] == date_most_recent, 'lifetime_total_likes']
    if likes_recent.shape[0] > 1:
        print('Duplicate records exist for client {} in 1_fb_page_insights'.format(client_id))

    likes_recent = likes_recent.values[0]

    return likes_recent, date_most_recent


def plot_df_for_recent_subset(client_id, column, last_n_days, datetime_col):
    df = get_df_fb_page_insights(client_id)
    df_subset = subset_df_for_last_n_days(df, last_n_days, datetime_col)
    df_subset_preprocessed = preprocess_timeseries(df=df_subset, column=column,
                                                   frequency='D', aggregation_function='last')
    return df_subset_preprocessed


def plot_df(client_id, column):
    df = get_df_fb_page_insights(client_id)
    df = preprocess_timeseries(df=df, column=column, frequency='D', aggregation_function='first')

    return df


def get_df_fb_list_of_posts_of_last_n_days(client_id, last_n_days):
    df = get_df_fb_list_of_posts(client_id)
    df = subset_df_for_last_n_days(df=df, last_n_days=last_n_days, datetime_col='created_time')

    return df


