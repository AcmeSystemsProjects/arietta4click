import tornado.ioloop
import tornado.web
import acmepins

class REL1_on(tornado.web.RequestHandler):
	def get(self):
		REL1.on() 
		print "REL1 ON"
		self.write("REL1 ON")

class REL1_off(tornado.web.RequestHandler):
	def get(self):
		REL1.off() 
		print "REL1 OFF"
		self.write("REL1 OFF")

application = tornado.web.Application([
	(r"/rel1_on", REL1_on),
	(r"/rel1_off", REL1_off),
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "RELAY_click.html"}),
])

if __name__ == "__main__":
	REL1 = acmepins.Pin('mikroBUS.1.PWM','out')
	REL2 = acmepins.Pin('mikroBUS.1.CS' ,'out')

	application.listen(8080,"0.0.0.0")
	tornado.ioloop.IOLoop.instance().start()
