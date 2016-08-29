#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2

class ActionPage(webapp2.RequestHandler):

    def get(self, action):

        self.response.headers['Content-Type'] = 'text/plain'        
        self.response.out.write('Action, ' + action)

class MainPage(webapp2.RequestHandler):

    def get(self):

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, webapp2 World!')

app = webapp2.WSGIApplication([
        webapp2.Route(r'/<action:(start|failed)>', handler=ActionPage),
        webapp2.Route(r'/', handler=MainPage),                    
], debug=True)
