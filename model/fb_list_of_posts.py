import pandas as pd

from model.core import df_from_db_with_date_format_col

client_id_ = 'soc_prasad'


def get_df_fb_list_of_posts(client_id):
    db_path_from_root = '/Users/abhilash/Insofe/Projects/socialight/app/insights_app/model/database/2_fb_list_of_posts.xlsx'
    df = df_from_db_with_date_format_col(client_id=client_id, db_path=db_path_from_root, datetime_col='created_time')
    return df

#def media_type
