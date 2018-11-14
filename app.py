from memory_profiler import profile

import tornado.ioloop
import tornado.web

import time

import uuid
import mimetypes
import os
import json

__UPLOADS__ = "/tmp/uploads/"

class PredictHandler(tornado.web.RequestHandler):

    def validate(self, body):
        return True

    async def post(self):

        fileinfo = self.request.files['filearg'][0]
        print ("fileinfo is", fileinfo)
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'wb')
        fh.write(fileinfo['body'])
        r = json.dumps({'result': True})
        self.write(r)
        #self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)

 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world 2")

@profile
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/predict", PredictHandler),
    ])

@profile
def main():
    print ('Hello, world!')

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    main()
    tornado.ioloop.IOLoop.current().start()

 

