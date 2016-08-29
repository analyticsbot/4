#!/usr/bin/env python

#import all required libraries
import webapp2
import json
import time
import cachetools
from google.appengine.ext import ndb
from google.appengine.api import memcache
import operator
from datetime import datetime

## declaring static variables
PREFIXES = ['reasonginserver', 'defaultrecs']## prefixes for the key
TOP_N = 5## number of default articles

## initializing cache
cache_recs = cachetools.LRUCache(maxsize=5000) ## holds local cache for recommendations
cache = cachetools.LRUCache(maxsize=10000) ## holds all other types of cache

## Sample Models as per information provided by the entities 
## that might be used. Just for my reference and client's understanding on
## the structure

class Templates(ndb.Model):
    """ Model class for templates for testing """
    appId = ndb.StringProperty()
    articleIdSelector = ndb.StringProperty()
    articleTitleSelector = ndb.StringProperty()
    articleSubtitleSelector = ndb.StringProperty()
    articleBodySelector = ndb.StringProperty()
    articlegenomeServer = ndb.StringProperty()
    baseurl = ndb.StringProperty()
    renderMethod = ndb.StringProperty()

class Recommendations(ndb.Model):
    """Model class for Recommendations for testing"""
    articleId  = ndb.StringProperty() 
    title = ndb.StringProperty()
    keywords = ndb.StringProperty()
    tags  = ndb.StringProperty()

class MyData(ndb.Model):
    """Model class for Key/value pair for testing"""
    keyString = db.StringProperty()
    valueString = db.StringProperty()

class Default_Reccommendations(db.Model):
    """Model class for Default Recommendations for testing"""
    myKey = db.StringProperty(required=True)
    myTopArticles = db.StringProperty(required=True)

## Defining all the required handlers 

class JavascriptHandler(webapp2.RequestHandler):
    """Handler for '/XX/articleinject.js?ver=QQ' api' """

    def get(self, app = None):
        """ get function to handle the get requests to JavascriptHandler
            self.ver = the version of the template required       
            self.app = application name
            self.temp_key = key name for the template
            self.appdata_key = key name for the appdata
            self.instantiated_template_key = key name for the instantiated template
            self.template_in_cache = boolean to check whether template in cache
            self.appdata_in_cache = boolean to check whether appdata in cache
        """

        self.ver = self.request.get('ver')        
        self.app = app
        self.temp_key = 'jstemplate:v' + self.ver
        self.time_temp_key = 'time_jstemplate:v' + self.ver
        self.appdata_key = 'appdata:' + self.app
        self.time_appdata_key = 'time_appdata:' + self.app
        self.instantiated_template_key = 'instantiated:' + self.ver + ':' + self.app
        self.appData_in_cache = True
        self.template_in_cache = True

        ## retreive last time template was fetched from cache
        ## if time > 4 hours(14400), request from memcache
        ## if not in memcache, request from datastore. Add to memcache. Add to local cache
        
        template_time = cache.get(self.time_temp_key)

        if template_time is not None:
            curr_time = datetime.now()
            delta = curr_time - template_time
            if delta.total_seconds() > 14400:
                ## last fetch was more than 4 hours ago. fetch from memcache/datastore
                template = memcache.get(self.temp_key)
                if template is None:
                    template_in_cache = False
                    template_key = ndb.key('Templates', self.temp_key) ## Change 'Templates' with the actual entity name
                    template = template_key.get()

                    # add to template to memcache and template as well as time to local cache
                    memcache.add(self.temp_key, template)
                    cache.update([(self.temp_key, template)])
                    cache.update([(self.time_temp_key, datetime.now())])

            else:
                ## less than 4 hours old entry exists in cache. fetch it
                template = cache.get(self.temp_key)
            
        else:
            template = memcache.get(self.temp_key)
            cache.update([(self.time_temp_key, datetime.now())]) ## if the template was available in memcache

            if template is None:
                template_in_cache = False
                template_key = ndb.key('Templates', self.temp_key) ## Change 'Templates' with the actual entity name
                template = template_key.get()

                # add to template to memcache and template as well as time to local cache
                memcache.add(self.temp_key, template)
                cache.update([(self.temp_key, template)])
                cache.update([(self.time_temp_key, datetime.now())])


        ## retreive last time appdata was fetched from cache
        ## if time > 4 hours(14400), request from memcache
        ## if not in memcache, request from datastore. Add to memcache. Add to local cache
        
        appdata_time = cache.get(self.time_appdata_key)

        if appdata_time is not None:
            curr_time = datetime.now()
            delta = curr_time - appdata_time
            if delta.total_seconds() > 14400:
                ## last fetch was more than 4 hours ago. fetch from memcache/datastore
                appData = memcache.get(self.appdata_key)
                cache.update([(self.time_appdata_key, datetime.now())]) ## if the template was available in memcache
                appData_in_cache = False
                if appData is None:
                    appData_in_cache = False
                    appData_key = ndb.key('ApplicationData', self.appdata_key) ## Change 'Templates' with the actual entity name
                    appData = appData_key.get()

                    # add to template to memcache and template as well as time to local cache
                    memcache.add(self.appdata_key, appData)
                    cache.update([(self.appdata_key, appData)])
                    cache.update([(self.time_appdata_key, datetime.now())])

            else:
                ## less than 4 hours old entry exists in cache. fetch it
                appData = cache.get(self.appdata_key)
            
        else:
            appData = memcache.get(self.appdata_key)
            cache.update([(self.time_appdata_key, datetime.now())]) ## if the template was available in memcache
            appData_in_cache = False
            if appData is None:
                appData_in_cache = False
                appData_key = ndb.key('ApplicationData', self.appdata_key) ## Change 'Templates' with the actual entity name
                appData = appData_key.get()

                # add to template to memcache and template as well as time to local cache
                memcache.add([(self.appdata_key, appData)])
                cache.update([(self.appdata_key, appData)])
                cache.update([(self.time_appdata_key, datetime.now())])


        ## check whether both template and app data found from cache
        ## else if anyone is false, recalculate the value by
        ## replacing the key with the values from appData
        ## and store back to local cache
        ## else if both true retrieve from local cache
        if self.appData_in_cache and self.template_in_cache:
            return cache.get(self.instantiated_template_key)
        else:
            for key, value in appData:
                template.replace('{{' + key + '}}', value)
            
            cache.update([(self.instantiated_template_key, template)])
        
        return template
        

class RecommendationsHandler(webapp2.RequestHandler):
    """Handler for /getRecommendations?appId=XX&articleId=YY&clientId=ZZ api """

    def get(self):
        """get function to handle the get requests to RecommendationsHandler
        self.appId = application id
        self.articleId = article id
        self.clientId = client id
        self.recommendation_key = recommendation key based on application id and article id
        self.requestedpull = request pull key
        self.default_recs_key = default recommendation key
        self.counter_key = key for the counter for the articles
        """

        self.appId = self.request.get('appId')
        self.articleId = self.request.get('articleId')
        self.clientId = self.request.get('clientId')
        self.recommendation_key = 'rec:' + self.appId + ':' + self.articleId
        self.requestedpull_key = 'requestedpull:' + self.appId + ':' + self.articleId
        self.default_recs_key = 'defaultrecs:' +  self.appId
        self.counter_key = 'articleCounter'  
        self.appid_key = 'appdata:' + self.appId
        self.reasoningserver_key = 'reasoningserver:' + self.appId  

        ## get recommendations from local cache. Else
        ## if not found get data from memcache. If not found get from datastore
        recs = cache_recs.get(self.recommendation_key)    
        if recs is None:
            ## no recommendations found in local cache
            ## pull from memcache. else from datastore    
            recs = memcache.get(self.recommendation_key)
            if recs:
                cache_recs.update([(self.recommendation_key, recs)])
                ## get the counter ticker from the cache
                ## if not found, initialize as a dictionary
                ## if found, check whether the current value is present
                ## if yes, add one the count. Else add the key
                counterTicker = cache.get(self.counter_key)
                if counterTicker is None:
                    counterTicker = {}
                    counterTicker[self.appId + '/' + self.articleId] = 1
                else:
                    if (self.appId + '/' + self.articleId) not in counterTicker.keys():
                        counterTicker[self.appId + '/' + self.articleId] = 1
                    else:
                        counterTicker[self.appId + '/' + self.articleId] += 1            

                return {'status': 'found', 'recs': recs}

            else:
                recs_key = ndb.key('Recommendations', self.recommendation_key)
                recs = recs_key.get()
           
                memcache.add(self.recommendation_key, recs)
                cache_recs.update([(self.recommendation_key, recs)])

                ## get app data from cache else get from datastore
                appData = memcache.get(self.appid_key)
                if appData is None:
                    appData_key = ndb.key('ApplicationData', self.appid_key)
                    appData = appData_key.get()
               
                    memcache.add(self.appid_key, appData) 

                ## get lastRequested from memcache else get from datastore
                lastRequested = memcache.get(self.requestedpull_key)
                if lastRequested is None:
                    lastRequested = datetime.now()

                    memcache.add(self.requestedpull_key, lastRequested, time=3600)
                
                ## seconds since last request
                seconds_since_last_request = (datetime.now() - lastRequested).total_seconds()

                ## get default recs from 
                default_recs = memcache.get(self.default_recs_key)
                if default_recs is None:
                    default_recs_key = ndb.key('Default_Reccommendations', self.default_recs_key)
                    default_recs = default_recs_key.get()
               
                    memcache.add(self.default_recs_key, default_recs)

                ## get reasoning server from memcache else get from datastore
                reasoning_server = memcache.get(self.reasoning_server_key)
                if reasoning_server is None:
                    reasoning_server_key = ndb.key('Reasoning Server', self.reasoning_server)
                    reasoning_server = reasoning_server_key.get()

                    memcache.add(self.reasoning_server_key, reasoning_server)

                ## if seconds_since_last_request then return back another key "should_request" with
                ## value reasoning_server
                if seconds_since_last_request > 5:
                    return {'status': 'not found', 'recs': default_recs, 'appData': appData, 'should_request': reasoning_server}
                else:
                    return {'status': 'not found', 'recs': default_recs, 'appData': appData}


class RegisterClickHandler(webapp2.RequestHandler):
    """Handler for /registerClick?appId=XX&&articleId=YY&clientId=ZZ&relatedArticleId=RR api """

    def get(self):
        """get function to handle the get requests to RegisterClickHandler
        self.appId = application id
        self.articleId = article id
        self.clientId = client id
        self.relatedArticleId = related article id
        """
        self.appId = self.request.get('appId')
        self.articleId = self.request.get('articleId')
        self.clientId = self.request.get('clientId')
        self.relatedArticleId = self.request.get('relatedArticleId')

        logging.info('User : ' + self.clientId + ' clicked on article : ' + self.articleId)

        return {'status':'success'}

class StoreHandler(webapp2.RequestHandler):
    """Handler for /store?token=TOKEN&key=KEY&value=VALUE api"""

    def get(self):
        self.post()

    def post(self):
        self.key = self.request.get('key')
        self.value = self.request.get('value')
        self.token = self.request.get('token')

        if self.key.startswith(PREFIXES):
            ## replace MyData with actual entity
            values = ndb.GqlQuery("SELECT * FROM MyData WHERE keyString = '%s'" % self.key) 
            if values.count() > 0:
              data = values[0]
            else:
              data = MyData()
              data.valueString = self.value
              data.keyString = self.key
              data.put()

            return {'status':'success'}
        else:
            return {'status':'failure'}


class TaskHandler(webapp2.RequestHandler):
    """Handler for /task/updateDefaultRecs api"""

    def get(self):
        self.counter_key = 'articleCounter' 
        counterTicker = cache.get(self.counter_key)

        ## copy the counter
        counterTicker_copy = counterTicker

        ## empty the counter value in cache 
        cache.pop(self.counter_key)

        defaultrecs = {}

        for key, value in counterTicker.iteritems():
            appid_articleid = key
            appid = key.split('/')[0]
            articleid = key.split('/')[1]
            count = value

            if appid not in defaultrecs.keys():
                defaultrecs[appid] = {}
            else:
                if articleid not in defaultrecs[appid].keys():
                    defaultrecs[appid][articleid] = 0
                else:
                    defaultrecs[appid][articleid] += count

        for key, value in defaultrecs.iteritems():
            app_key = 'defaultrecs:' + key
            app_articles = value
            sorted_app_articles = sorted(app_articles.items(), key = operator.itemgetter(1), reverse = True)[:TOP_N]
            data = Default_Reccommendations(myKey = app_key, myTopArticles = sorted_app_articles)
            data.put()


app = webapp2.WSGIApplication([
    webapp2.Route('/<app>/articleinject.js', JavascriptHandler),
    ('/getRecommendations', RecommendationsHandler),
    ('/registerClick', RegisterClickHandler),
    ('/store', StoreHandler),
    ('/task/updateDefaultRecs', TaskHandler),
    ], debug=True)
