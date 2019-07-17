
import jinja2
import webapp2
import os
import urllib

from google.appengine.api import users

#CONSTANTS

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        url_logout = users.create_logout_url('/')

        template_values = {
            'user' : user,
            'url_logout' : url_logout,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
