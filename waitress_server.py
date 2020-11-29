from waitress import serve
import webapp
serve(webapp.app, host='0.0.0.0', port=5000)

