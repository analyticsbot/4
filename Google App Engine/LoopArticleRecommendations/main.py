#!/usr/bin/env python
# import all required libraries
import operator
import json
import logging
from datetime import datetime
import webapp2
import cachetools
from google.appengine.ext import ndb
from google.appengine.api import memcache

# declaring static variables
PREFIXES = ('appdata', 'jstemplate', 'rec', 'reasonginserver', 'defaultrecs')  # prefixes for the key
TOP_N = 5  # number of default articles

# initializing cache
# holds local cache for recommendations
cache_recs = cachetools.LRUCache(maxsize=5000)
cache = cachetools.LRUCache(maxsize=10000)  # holds all other types of cache

class appdata(ndb.Model):
    """ Model class for templates for testing """
    appJson = ndb.JsonProperty()
a = appdata()
a.appJson = json.dumps({ "appId": "EA45BD7D", "articleIdSelector": "body span.articleid", "articleTitleSelector": "article > div.title", "articleSubtitleSelector": "article div.subtitle", "articleBodySelector": "article", "articlegenomeServer": "modelviewer.loop.ai:8400/", "baseurl": "http://localhost/", "renderMethod": "slidein" })
a.key = ndb.Key('appdata', 'XX')
a.put()

class jstemplate(ndb.Model):
    """ Model class for templates for testing """
    templateString = ndb.StringProperty()
t =  jstemplate()
t.templateString = 'var appId = {{appId}}; var articleIdSelector = {{articleIdSelector}}; var articleTitleSelector = {{articleTitleSelector}}; var articleSubtitleSelector = {{articleSubtitleSelector}}; var articleBodySelector = {{articleBodySelector}}; var articlegenomeServer = {{articlegenomeServer}}; var baseurl = {{baseurl}}; var renderMethod = {{renderMethod}};'
t.key = ndb.Key('jstemplate', 'vQQ')
t.put()

class rec(ndb.Model):
    """Model class for Recommendations for testing"""
    recommendation = ndb.JsonProperty()
r = rec()
r.recommendation = json.dumps({"articleId":"ABCD1234","title":"News event just occurred!", "keywords":["news","events"],
"tags":["Happenings","Noteworthy"]})
r.key = ndb.Key('rec', 'XX:YY')
r.put()

class defaultrecs(ndb.Model):
    """Model class for Default Recommendations for testing"""
    defrecommendation = ndb.JsonProperty()
d = defaultrecs()
d.defrecommendation = json.dumps({'XX' : [{"articleId":"ABCD1234","title":"News event just occurred!", "keywords":["news","events"],
"tags":["Happenings","Noteworthy"]}]})
d.key = ndb.Key('defaultrecs', 'XX')
d.put()

class reasoningserver(ndb.Model):
    """Model class for Default Recommendations for testing"""
    reasonginservervalue = ndb.StringProperty()
rs = reasoningserver()
rs.reasonginservervalue = 'http://localhost'
rs.key = ndb.Key('reasoningserver', 'XX')
rs.put()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, World!')

# Defining all the required handlers
class JavascriptHandler(webapp2.RequestHandler):
    """Handler for '/XX/articleinject.js?ver=QQ' api' """

    def get(self, app_nm = None):
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
        self.app_ = app_nm
        self.temp_key = 'v' + self.ver
        self.time_temp_key = 'time_jstemplate:v' + self.ver
        self.appdata_key = self.app_
        self.time_appdata_key = 'time_appdata:' + self.app_
        self.instantiated_template_key = 'instantiated:' + self.ver + ':' + self.app_
        self.appData_in_cache = True
        self.template_in_cache = True

        # retreive last time template was fetched from cache
        # if time > 4 hours(14400), request from memcache
        # if not in memcache, request from datastore. Add to memcache. Add to
        # local cache
        template_time = cache.get(self.time_temp_key)

        if template_time is not None:
            curr_time = datetime.now()
            delta = curr_time - template_time
            if delta.total_seconds() > 14400:
                # last fetch was more than 4 hours ago. fetch from
                # memcache/datastore
                template = memcache.get(self.temp_key)
                if template is None:
                    self.template_in_cache = False
                    # Change 'Templates' with the actual entity name
                    #template = Templates.query(Templates.key == ndb.Key('Templates', 'vQQ')).fetch(1)
                    template_key = ndb.Key('jstemplate', self.temp_key)
                    template = template_key.get().templateString
                    #print 'template', template

                    # add to template to memcache and template as well as time
                    # to local cache
                    memcache.add(self.temp_key, template)
                    cache.update([(self.temp_key, template)])
                    cache.update([(self.time_temp_key, datetime.now())])

            else:
                # less than 4 hours old entry exists in cache. fetch it
                template = cache.get(self.temp_key)

        else:
            template = memcache.get(self.temp_key)
            #self.response.write(template)
            # if the template was available in memcache
            cache.update([(self.time_temp_key, datetime.now())])

            if template is None:
                self.template_in_cache = False
                # Change 'Templates' with the actual entity name
                #template = Templates.query(Templates.key == ndb.Key('Templates', 'vQQ')).fetch(1)
                template_key = ndb.Key('jstemplate', self.temp_key)
                template = template_key.get().templateString
                #self.response.write(template)

                # add to template to memcache and template as well as time to
                # local cache
                memcache.add(self.temp_key, template)
                cache.update([(self.temp_key, template)])
                cache.update([(self.time_temp_key, datetime.now())])

        # retreive last time appdata was fetched from cache
        # if time > 4 hours(14400), request from memcache
        # if not in memcache, request from datastore. Add to memcache. Add to
        # local cache

        appdata_time = cache.get(self.time_appdata_key)

        if appdata_time is not None:
            curr_time = datetime.now()
            delta = curr_time - appdata_time
            if delta.total_seconds() > 14400:
                # last fetch was more than 4 hours ago. fetch from
                # memcache/datastore
                appData = memcache.get(self.appdata_key)
                # if the template was available in memcache
                cache.update([(self.time_appdata_key, datetime.now())])
                self.appData_in_cache = False
                if appData is None:
                    self.appData_in_cache = False
                    # Change 'Templates' with the actual entity name
                    appData_key = ndb.Key('appdata', self.appdata_key)
                    appData = dict(json.loads(appData_key.get().appJson))
                    # add to template to memcache and template as well as time
                    # to local cache
                    memcache.add(self.appdata_key, appData)
                    cache.update([(self.appdata_key, appData)])
                    cache.update([(self.time_appdata_key, datetime.now())])

            else:
                # less than 4 hours old entry exists in cache. fetch it
                appData = cache.get(self.appdata_key)

        else:
            appData = memcache.get(self.appdata_key)
            # if the template was available in memcache
            cache.update([(self.time_appdata_key, datetime.now())])
            self.appData_in_cache = False
            if appData is None:
                self.appData_in_cache = False
                # Change 'ApplicationData' with the actual entity name
                appData_key = ndb.Key('appdata', self.appdata_key)
                appData = dict(json.loads(appData_key.get().appJson))

                # add to template to memcache and template as well as time to
                # local cache
                memcache.add(self.appdata_key, appData)
                cache.update([(self.appdata_key, appData)])
                cache.update([(self.time_appdata_key, datetime.now())])

        # check whether both template and app data found from cache
        # else if anyone is false, recalculate the value by
        # replacing the key with the values from appData
        # and store back to local cache
        # else if both true retrieve from local cache       
        if (self.appData_in_cache and self.template_in_cache):
            return self.response.write(str(cache.get(self.instantiated_template_key)))
        else:
            for key, value in appData.iteritems():
                template = template.replace('{{' + key + '}}', value)

            cache.update([(self.instantiated_template_key, template)])
        
        return self.response.write(str(template))


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
        self.recommendation_key = self.appId + ':' + self.articleId
        self.requestedpull_key = 'requestedpull:' + self.appId + ':' + self.articleId
        self.default_recs_key = self.appId
        self.default_recs_memcache_key = 'defaultrecs:' + self.appId
        self.counter_key = 'articleCounter'
        self.appid_key = 'appdata:' + self.appId
        self.reasoning_server_key = self.appId
        self.reasoning_server_memcache_key = 'reasoningserver:' + self.appId
        self.appdata_key = self.appId

        # get recommendations from local cache. Else
        # if not found get data from memcache. If not found get from datastore
        
        recs = cache_recs.get(self.recommendation_key)
        if recs is None:
            # no recommendations found in local cache
            # pull from memcache. else from datastore
            recs = memcache.get(self.recommendation_key)
            if recs is not None:                
                # get the counter ticker from the cache
                # if not found, initialize as a dictionary
                # if found, check whether the current value is present
                # if yes, add one the count. Else add the key
                counterTicker = cache.get(self.counter_key)
                if counterTicker is None:
                    counterTicker = {}
                    counterTicker[self.appId + '/' + self.articleId] = 1
                else:
                    if (self.appId + '/' +
                            self.articleId) not in counterTicker.keys():
                        counterTicker[self.appId + '/' + self.articleId] = 1
                    else:
                        counterTicker[self.appId + '/' + self.articleId] += 1
                
                cache.update([(self.counter_key, counterTicker)])
                cache_recs.update([(self.recommendation_key, recs)])
                
                return self.response.write({'status': 'found', 'recs': recs})

            else:
                # get recs from datastore, does not exists in memcache or local cache
                recs_key = ndb.Key('rec', self.recommendation_key)
                try:
                    recs = dict(json.loads(recs_key.get().recommendation))

                    counterTicker = cache.get(self.counter_key)
                    if counterTicker is None:
                        counterTicker = {}
                        counterTicker[self.appId + '/' + self.articleId] = 1
                    else:
                        if (self.appId + '/' +
                                self.articleId) not in counterTicker.keys():
                            counterTicker[self.appId + '/' + self.articleId] = 1
                        else:
                            counterTicker[self.appId + '/' + self.articleId] += 1
                    
                    cache.update([(self.counter_key, counterTicker)])

                except:
                    recs = None

                if recs is not None:
                    memcache.add(self.recommendation_key, recs)
                    cache_recs.update([(self.recommendation_key, recs)])

                    return self.response.write({'status': 'found', 'recs': recs})

                else:
                    # recs are not found, even in data store

                    # get app data from cache else get from datastore
                    appData = memcache.get(self.appid_key)
                    if appData is None:
                        appData_key = ndb.Key('appdata', self.appdata_key)
                        appData = dict(json.loads(appData_key.get().appJson))

                        memcache.add(self.appid_key, appData)

                    # get lastRequested from memcache else get from datastore
                    lastRequested = memcache.get(self.requestedpull_key)
                    if lastRequested is None:
                        lastRequested = datetime.now()

                        memcache.add(
                            self.requestedpull_key,
                            lastRequested,
                            time=3600)

                    # seconds since last request
                    seconds_since_last_request = (
                        datetime.now() - lastRequested).total_seconds()

                    # get default recs from
                    default_recs = memcache.get(self.default_recs_memcache_key)
                    if default_recs is None:
                        default_recs_key = ndb.Key('defaultrecs', self.default_recs_key)
                        default_recs = (default_recs_key.get().defrecommendation)

                        memcache.add(self.default_recs_memcache_key, default_recs)

                    # get reasoning server from memcache else get from datastore
                    reasoning_server = memcache.get(self.reasoning_server_memcache_key)
                    if reasoning_server is None:
                        reasoning_server_key_value = ndb.Key(
                            'reasoningserver', self.reasoning_server_key)
                        reasoning_server = reasoning_server_key_value.get().reasonginservervalue

                        memcache.add(self.reasoning_server_memcache_key, reasoning_server)

                    # if seconds_since_last_request then return back another key "should_request" with
                    # value reasoning_server
                    if seconds_since_last_request > 5:
                        return self.response.write({
                            'status': 'not found',
                            'recs': default_recs,
                            'appData': appData,
                            'should_request': reasoning_server})
                    else:
                        return self.response.write({
                            'status': 'not found',
                            'recs': default_recs,
                            'appData': appData})
        else:
            counterTicker = cache.get(self.counter_key)
            if counterTicker is None:
                counterTicker = {}
                counterTicker[self.appId + '/' + self.articleId] = 1
            else:
                if (self.appId + '/' +
                        self.articleId) not in counterTicker.keys():
                    counterTicker[self.appId + '/' + self.articleId] = 1
                else:
                    counterTicker[self.appId + '/' + self.articleId] += 1
            
            cache.update([(self.counter_key, counterTicker)])
            
            return self.response.write({'status': 'found', 'recs': recs})


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

        logging.info(
            'User : ' +
            self.clientId +
            ' clicked on article : ' +
            self.articleId)

        return self.response.write({'status': 'success'})


class StoreHandler(webapp2.RequestHandler):
    """Handler for /store?token=TOKEN&key=KEY&value=VALUE api"""

    def get(self):
        self.key = self.request.get('key')
        self.value = self.request.get('value')
        self.token = self.request.get('token')
        self.post()

    def post(self):
        """ post method 
        self.key = key
        self.value = value for the key
        self.token = token
        """        

        if self.key.startswith(PREFIXES):
            # replace MyData with actual entity
            class_ = self.key.split(':')[0]
            key_ = self.key.split(':')[1]
            valueString = self.value

            if class_ == 'reasonginserver':
                rs =  reasonginserver()
                rs.key = ndb.key('reasonginserver', key_)
                rs.reasonginservervalue = valueString
                rs.put()
                return self.response.write({'status': 'success'})

            elif class_ == 'jstemplate':
                js =  jstemplate()
                js.key = ndb.Key('jstemplate', key_)
                js.templateString = valueString
                js.put()
                return self.response.write({'status': 'success'})

            elif class_ == 'appdata':
                ap =  appdata()
                ap.key = ndb.Key('appdata', key_)
                ap.appJson = valueString
                ap.put()
                return self.response.write({'status': 'success'})

            elif class_ == 'rec':
                rc =  rec()
                rc.key = ndb.Key('rec', key_)
                rc.recommendation = valueString
                rc.put()
                return self.response.write({'status': 'success'})

            elif class_ == 'defaultrecs':
                df =  defaultrecs()
                df.key = ndb.Key('defaultrecs', key_)
                df.defrecommendation = valueString
                df.put()
                return self.response.write({'status': 'success'})

            else:
                self.response.write({'status': 'failure'})

        else:
            return self.response.write({'status': 'failure'})


class TaskHandler(webapp2.RequestHandler):
    """Handler for /task/updateDefaultRecs api"""

    def get(self):
        """ get method. Runs every 20 minutes
        self.counter_key = the key for counter of articles
        counterTicker = dictionary of articles viewed
        """
        self.counter_key = 'articleCounter'
        counterTicker = cache.get(self.counter_key)

        # copy the counter
        counterTickerCopy = counterTicker

        # # empty the counter value in cache
        try:
            cache.pop(self.counter_key)
        except:
            pass

        defaultrecs = {}

        try:
            for key, value in counterTickerCopy.iteritems():
                appid = key.split('/')[0]
                articleid = key.split('/')[1]
                count = value
                    
                if appid not in defaultrecs.keys():
                    defaultrecs[appid] = {}
                    defaultrecs[appid][articleid] = count
                else:
                    if articleid not in defaultrecs[appid].keys():
                        defaultrecs[appid][articleid] = 0
                    else:
                        defaultrecs[appid][articleid] += count
            
            for key, value in defaultrecs.iteritems():
                app_articles = value
                sorted_app_articles = sorted(
                    app_articles.items(),
                    key=operator.itemgetter(1),
                    reverse=True)[:TOP_N]
                data = DefaultReccommendations()
                data.defrecommendation = json.dumps({key : [(key + ':' + i[0]) for i in sorted_app_articles]})
                data.key = ndb.Key('DefaultReccommendations', key)
                data.put()
            
        except:
            pass


app = webapp2.WSGIApplication([
    webapp2.Route(r'/<app_nm>/articleinject.js', handler = JavascriptHandler, name='app_name'),
    (r'/getRecommendations', RecommendationsHandler),
    (r'/registerClick', RegisterClickHandler),
    (r'/store', StoreHandler),
    (r'/task/updateDefaultRecs', TaskHandler),
    (r'/', MainHandler)
], debug=True)
