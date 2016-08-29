from facebookads import FacebookSession
from facebookads import FacebookAdsApi
from facebookads.objects import (
    AdUser,
    Campaign,
)
from sqlalchemy import create_engine, MetaData
import json, os, pprint, time, sys

pp = pprint.PrettyPrinter(indent=4)
this_dir = os.path.dirname(__file__)
config_filename = os.path.join(this_dir, 'config.json')

config_file = open(config_filename)
config = json.load(config_file)
config_file.close()

### Setup session and api objects
session = FacebookSession(
    config['app_id'],
    config['app_secret'],
    config['access_token'],
)
api = FacebookAdsApi(session)
debug  = True
database = 'postgresql://postgres:postgres@localhost/transformair'
## initiate the db connection to postgres
#engine = create_engine('postgresql://postgres:postgres@localhost/transformair')
try:
    con = create_engine(database, client_encoding='utf8')
    meta = MetaData(bind=con, reflect=True)

    if debug:
        print 'Connection to db made successfully'
except:
    if debug:
        print 'Error connecting to db. Check connection string or if the db is up and running'
    sys.exit(1)

exp = meta.tables['exp']
final = meta.tables['final']

if __name__ == '__main__':
    FacebookAdsApi.set_default_api(api)

    print('\n\n\n********** Reading objects example. **********\n')

    ### Setup user and read the object from the server
    me = AdUser(fbid='me')

    ### Get first account connected to the user
    my_account = me.get_ad_account()

    print('>>> Reading accounts associated with user')
    pp.pprint(my_account)
    time_range = {'since':'2016-04-29','until':'2016-04-29'}
    params_data = {'time_range':time_range}
    print(">>> Campaign Stats")
    for campaign in my_account.get_campaigns(fields=[Campaign.Field.name]):
        ad_sets = campaign.get_ads(fields = [AdUser.Field.name])
        for ad_set in ad_sets:
            time.sleep(10)
##            ad_data = ad_set.get_insights(params = params_data, fields = ['date_start', 'date_stop', 'account_id', \
##                                                'account_name', 'ad_id', 'ad_name', 'buying_type', \
##                                                'campaign_id', 'campaign_name', 'adset_id', \
##                                                'adset_name', 'objective', 'actions', \
##                                                'unique_actions', 'total_actions', \
##                                                'total_unique_actions', 'action_values', \
##                                                'total_action_value', 'impressions', \
##                                                'social_impressions', 'clicks', 'social_clicks', \
##                                                'unique_impressions', 'unique_social_impressions', \
##                                                'unique_clicks', 'unique_social_clicks', 'spend', \
##                                                'frequency', 'social_spend', 'deeplink_clicks', \
##                                                'app_store_clicks', 'website_clicks', \
##                                                'cost_per_inline_post_engagement', \
##                                                'inline_link_clicks', 'cost_per_inline_link_click', \
##                                                'inline_post_engagement', 'unique_inline_link_clicks',\
##                                                'cost_per_unique_inline_link_click', \
##                                                'inline_link_click_ctr', 'unique_inline_link_click_ctr',\
##                                                'call_to_action_clicks', 'newsfeed_avg_position', \
##                                                'newsfeed_impressions', 'newsfeed_clicks', 'reach', \
##                                                'social_reach', 'ctr', 'unique_ctr', \
##                                                'unique_link_clicks_ctr', 'cpc', 'cpm', 'cpp', \
##                                                'cost_per_total_action', 'cost_per_action_type', \
##                                                'cost_per_unique_click', 'cost_per_10_sec_video_view', \
##                                                'cost_per_unique_action_type', 'relevance_score', \
##                                                'website_ctr', 'video_avg_sec_watched_actions', \
##                                                'video_avg_pct_watched_actions', \
##                                                'video_p25_watched_actions', 'video_p50_watched_actions',\
##                                                'video_p75_watched_actions', 'video_p95_watched_actions', \
##                                                'video_p100_watched_actions', 'video_complete_watched_actions', \
##                                                'video_10_sec_watched_actions', 'video_15_sec_watched_actions', \
##                                                'video_30_sec_watched_actions', 'estimated_ad_recallers', \
##                                                'estimated_ad_recallers_lower_bound', \
##                                                'estimated_ad_recallers_upper_bound', 'estimated_ad_recall_rate', \
##                                                'estimated_ad_recall_rate_lower_bound', \
##                                                'estimated_ad_recall_rate_upper_bound', \
##                                                'cost_per_estimated_ad_recallers', 'canvas_avg_view_time', \
##                                                'canvas_avg_view_percent', 'place_page_name', 'ad_bid_type', \
##                                                'ad_bid_value', 'ad_delivery', 'adset_bid_type', 'adset_bid_value'])
            ad_data = ad_set.get_insights(params = params_data, fields = ['date_start', 'date_stop', 'account_id', \
                                                'account_name', 'ad_id', 'ad_name', \
                                                'campaign_id', 'campaign_name', 'adset_id', \
                                                'adset_name',  \
                                               
                                               'impressions', \
                                                'social_impressions', 'clicks', 'social_clicks', \
                                                'unique_impressions', 'unique_social_impressions', \
                                                'unique_clicks', 'unique_social_clicks', 'spend', \
                                                'frequency', 'social_spend', 'deeplink_clicks', \
                                                'app_store_clicks', 'website_clicks', \
                                                'cost_per_inline_post_engagement', \
                                                'inline_link_clicks', 'cost_per_inline_link_click', \
                                                'inline_post_engagement', 'unique_inline_link_clicks',\
                                                
                                                'inline_link_click_ctr', 'unique_inline_link_click_ctr',\
                                                'call_to_action_clicks', 'newsfeed_avg_position', \
                                                'newsfeed_impressions', 'newsfeed_clicks', 'reach', \
                                                'social_reach', 'ctr', 'unique_ctr', \
                                                'unique_link_clicks_ctr', 'cpc', 'cpm', 'cpp', \
                                                'cost_per_total_action', 
                                                'cost_per_unique_click', 'cost_per_10_sec_video_view', \
                                                  \
                                                 'video_avg_sec_watched_actions', \
                                                'video_avg_pct_watched_actions', \
                                                'video_p25_watched_actions', 'video_p50_watched_actions',\
                                                'video_p75_watched_actions', 'video_p95_watched_actions', \
                                                'video_p100_watched_actions', 'video_complete_watched_actions', \
                                                'video_10_sec_watched_actions', 'video_15_sec_watched_actions', \
                                                'video_30_sec_watched_actions', 'estimated_ad_recallers', \
                                                'estimated_ad_recallers_lower_bound', \
                                                'estimated_ad_recallers_upper_bound', 'estimated_ad_recall_rate', \
                                                'estimated_ad_recall_rate_lower_bound', \
                                                'estimated_ad_recall_rate_upper_bound', \
                                                'cost_per_estimated_ad_recallers', 'canvas_avg_view_time', \
                                                'canvas_avg_view_percent', 'place_page_name'])
            
            ad_dict= {}
            try:
                for key, value in ad_data[0].iteritems():
                    ad_dict[key] = value
            except:
                pass
            print ad_dict
            try:
                con.execute(meta.tables['exp'].insert(), ad_dict)
            except Exception,e:
                print str(e)
                pass


