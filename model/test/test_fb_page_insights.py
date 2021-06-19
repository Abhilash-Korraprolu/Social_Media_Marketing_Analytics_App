from model.fb_page_insights import get_lifetime_likes_meter_values, get_df_fb_page_insights

client_id_ = 'soc_prasad'


def test_get_dataframe_fb_page_insights_returns_df_with_important_columns_for_non_existant_client():
    df = get_df_fb_page_insights(client_id='dummy name')
    important_columns = ['daily_total_impressions', 'lifetime_total_likes']
    assert set(important_columns).issubset(df.columns)

def test_get_dataframe_fb_page_insights_returns_df_with_important_columns_for_existing_client():
    df = get_df_fb_page_insights(client_id=client_id_)
    important_columns = ['daily_total_impressions', 'lifetime_total_likes']
    assert set(important_columns).issubset(df.columns)

def test_get_lifetime_likes_meter_values_with_last_month_ago_data_present():
    cid = 'test_like_meter_1_month_ago_present'
    likes_recent, likes_month_ago = get_lifetime_likes_meter_values(client_id=cid)
    assert likes_recent == 100
    assert likes_month_ago == 10


def test_get_lifetime_likes_meter_values_with_more_than_last_month_ago_data_present():
    cid = 'test_like_meter_more_than_1_month_ago_present'
    likes_recent, likes_month_ago = get_lifetime_likes_meter_values(client_id=cid)
    assert likes_recent == 100
    assert likes_month_ago == 10


def test_get_lifetime_likes_meter_values_with_last_month_ago_data_not_present():
    cid = 'test_like_meter_1_month_ago_not_present'
    likes_recent, likes_month_ago = get_lifetime_likes_meter_values(client_id=cid)
    assert likes_recent == 100
    assert likes_month_ago == 0


def test_get_lifetime_likes_meter_values_when_no_client_id_records_present_in_the_database():
    cid = 'client_that_doesnt_exist'
    likes_recent, likes_month_ago = get_lifetime_likes_meter_values(client_id=cid)
    assert likes_recent == 0
    assert likes_month_ago == 0
