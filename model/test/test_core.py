from core import subset_df_for_last_n_days, df_from_db_with_date_format_col
from fb_page_insights import get_df_fb_page_insights


def test_subset_df_for_last_n_days():
    db_path_from_root = '/Users/abhilash/Insofe/Projects/socialight/app/insights_app/model/database/1_fb_page_insights.xlsx'
    datetime_col = 'datetime'
    df = df_from_db_with_date_format_col(client_id='soc_test', db_path=db_path_from_root, datetime_col=datetime_col)
    df_subset = subset_df_for_last_n_days(df=df, last_n_days=1, datetime_col=datetime_col)

    # The next recent record in the table is 1 month away. Hence this should return only the recent date record
    assert df_subset[datetime_col].min() == df_subset[datetime_col].max()
    assert df_subset.shape[0] == 1
