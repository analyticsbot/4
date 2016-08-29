# Sample Models as per information provided by the entities
# that might be used. Just for my reference and client's understanding on
# the structure


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

class ApplicationData(ndb.Model):
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
    articleId = ndb.StringProperty()
    title = ndb.StringProperty()
    keywords = ndb.StringProperty()
    tags = ndb.StringProperty()


class MyData(ndb.Model):
    """Model class for Key/value pair for testing"""
    keyString = db.StringProperty()
    valueString = db.StringProperty()


class DefaultReccommendations(db.Model):
    """Model class for Default Recommendations for testing"""
    myKey = db.StringProperty(required=True)
    myTopArticles = db.StringProperty(required=True)

“appId”: “EA45BD7D”,
“articleIdSelector”: “body span.articleid”,
“articleTitleSelector”: “article > div.title”,
“articleSubtitleSelector”: “article div.subtitle”,
“articleBodySelector”: “article”,
“articlegenomeServer”: “modelviewer.loop.ai:8400/”
“baseurl”: “http://localhost/”,
“renderMethod”: “slidein”