#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, urlparse


class SmsReceiver():
	class RequestHandler(BaseHTTPRequestHandler):
		def do_GET(self):
			# all responses from this handler are pretty much the
			# same - an http status and message - so let's abstract it!
			def respond(code, message):
				self.send_response(code)
				self.end_headers()
				
				# recycle the full HTTP status message if none were provided
				if message is None: message = self.responses[code][0]
				self.wfile.write(message)
			
			
			# explode the URI to pluck out the
			# query string as a dictionary
			parts = urlparse.urlsplit(self.path)
			vars = cgi.parse_qs(parts[3])
			
			
			# if this event is valid, then thank kannel, and
			# invoke the receiver function with the sms data
			if vars.has_key("callerid") and vars.has_key("message"):
				self.server.receiver(vars["callerid"][0], vars["message"][0])
				respond(200, "SMS Received OK")
			
			# the request wasn't valid :(
			else: respond(400)
		
		
		# we don't need to see every request in the console, since the
		# app will probably log it anyway. note: errors are still shown!
		def log_request(self, code="-", size="-"):
			pass
	
	
	def __init__(self, receiver):
		handler = self.RequestHandler
		self.serv = HTTPServer(("", 4500), handler)
		self.serv.receiver = receiver
	
	def run(self):
		self.serv.serve_forever()




# if this is invoked directly, test things out by
# listening for SMSs, and printing them to stdout
if __name__ == "__main__":
	class TestReceiver():
		def iGotAnSMS(self, caller, msg):
			print "SMS from %s: %s" % (caller, msg)
	
	tr = TestReceiver()
	print "Waiting for SMS..."
	SmsReceiver(tr.iGotAnSMS).run()

