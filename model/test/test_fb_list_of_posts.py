from model.fb_list_of_posts import get_df_fb_list_of_posts

client_id_ = 'soc_prasad'


def test_get_dataframe_fb_list_of_posts_returns_df_with_important_columns_for_non_existent_client():
    df = get_df_fb_list_of_posts(client_id='dummy name')
    important_columns = ['admin_creator', 'media_type', 'message']
    assert set(important_columns).issubset(df.columns)


def test_get_dataframe_fb_list_of_posts_returns_df_with_important_columns_for_existing_client():
    df = get_df_fb_list_of_posts(client_id=client_id_)
    important_columns = ['admin_creator', 'media_type', 'message']
    assert set(important_columns).issubset(df.columns)
