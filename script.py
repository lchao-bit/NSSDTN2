from mitmproxy.models import HTTPResponse
from netlib.http import Headers

import os
import re
import time
def request(context, flow):
    print flow.request.path
    m = re.match("^/geoserver/i/([\d]+)/([\d]+)/([\d]+)$", flow.request.path)
    if m is not None:
        print "match success!"
        imagename = flow.request.path_components[1] + '_' + flow.request.path_components[2] + '_' + flow.request.path_components[3] + '_' + flow.request.path_components[4];
        imagefilepath = "/home/dtn2/bpqrecv/" + imagename;
        print imagename
        print imagefilepath
        if(os.path.exists(imagefilepath)):
        	resp = HTTPResponse(
		"HTTP/1.1", 200, "OK", Headers(Content_Type="image/png"), "helloworld")
                with open(imagefilepath, 'r') as f:
             		payload = f.read()
             		resp.content = payload
             		resp.headers["Content-Length"] = str(len(payload))
                        resp.headers["Access-Control-Allow-Origin"] = "*"
                        print len(payload)
                        f.close()
                flow.reply(resp)
                
	else:
		querycomm = "/home/dtn2/dtn2/NSSDTN2/DTN2/apps/dtnquery/dtnquery -m send -s dtn://dtn1.dtn -d dtn://dtn2.dtn -q " + imagename + " -f " + imagefilepath;
		os.system(querycomm);
                waitingcomm = "/home/dtn2/dtn2/NSSDTN2/waiting " + imagename;
                os.system(waitingcomm);
        	resp = HTTPResponse(
		"HTTP/1.1", 200, "OK", Headers(Content_Type="image/png"), "helloworld")
                with open(imagefilepath, 'r') as f:
             		payload = f.read()
             		resp.content = payload
             		resp.headers["Content-Length"] = str(len(payload))
			resp.headers["Access-Control-Allow-Origin"] = "*"
                        print len(payload)
                        f.close()
                flow.reply(resp)
    v = re.match("^/geoserver/v/([\d]+)/([\d]+)/([\d]+)$", flow.request.path)
    if v is not None:
        vectorname = flow.request.path_components[1] + '_' +  flow.request.path_components[2] + '_' + flow.request.path_components[3] + '_' + flow.request.path_components[4];
        vectorfilepath = "/home/dtn2/bpqrecv/" + vectorname;
        if(os.path.exists(vectorfilepath)):
        	resp = HTTPResponse(
		"HTTP/1.1", 200, "OK", Headers(Content_Type="application/json"), "helloworld")
                with open(vectorfilepath, 'r') as f:
             		payload = f.read()
             		resp.content = payload
             		resp.headers["Content-Length"] = str(len(payload))
			resp.headers["Access-Control-Allow-Origin"] = "*"
                        print len(payload)
                        f.close()
                flow.reply(resp)
        else:
        	querycomm = "/home/dtn2/dtn2/NSSDTN2/DTN2/apps/dtnquery/dtnquery -m send -s dtn://dtn1.dtn -d dtn://dtn2.dtn -q " + vectorname + " -f " + vectorfilepath;
		os.system(querycomm);
                waitingcomm = "/home/dtn2/dtn2/NSSDTN2/waiting " + vectorname;
                os.system(waitingcomm);
		resp = HTTPResponse(
		"HTTP/1.1", 200, "OK", Headers(Content_Type="application/json"), "helloworld")
                with open(vectorfilepath, 'r') as f:
             		payload = f.read()
             		resp.content = payload
             		resp.headers["Content-Length"] = str(len(payload))
			resp.headers["Access-Control-Allow-Origin"] = "*"
                        print len(payload)
                        f.close()
                flow.reply(resp)
    resp = HTTPResponse(
		"HTTP/1.1", 404, "Not Found", Headers(Content_Type="text/html"), "Not Found")
    resp.headers["Content-Length"] = str(len("Not Found"))
    flow.reply(resp)
