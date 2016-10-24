from mitmproxy.models import HTTPResponse
from netlib.http import Headers
from mitmproxy.script import concurrent
from subprocess import Popen, PIPE
import os
import re
import time
import sys
import subprocess
import random
import string
import signal
@concurrent
def request(context, flow):
    print flow.request.path
    m = re.match("^/geoserver/i/([\d]+)/([\d]+)/([\d]+)$", flow.request.path)
    if m is not None:
        print "match success!"
        imagename = flow.request.path_components[1] + '_' + flow.request.path_components[2] + '_' + flow.request.path_components[3] + '_' + flow.request.path_components[4];
        imagequerycache = "/home/root/accesscache " + imagename;
        imagequerycacheresult = os.popen(imagequerycache).read();
        if (imagequerycacheresult != "No" and imagequerycacheresult != "ERROR"):
        	resp = HTTPResponse(
		"HTTP/1.1", 200, "OK", Headers(Content_Type="image/png"), "helloworld")
                with open(imagequerycacheresult, 'r') as f:
             		payload = f.read()
             		resp.content = payload
             		resp.headers["Content-Length"] = str(len(payload))
                        resp.headers["Access-Control-Allow-Origin"] = "*"
                        print len(payload)
                        f.close()
                flow.reply(resp)
                return
	else:
		imagefilepath = "/home/root/bpqrecv/" + imagename;
                randregid = randrange(0, 32768);
		print randregid;
		querycomm = "/home/root/DTN2/apps/dtnquery/dtnquery -m send -s dtn://dtn1.dtn -d dtn://dtn2.dtn -q " + imagename + " -i " + str(randregid);
                print querycomm;
		os.system(querycomm);
                for x in range(0, 60):
			imagequerycacheresult = os.popen(imagequerycache).read();
			if (imagequerycacheresult != "No" and imagequerycacheresult != "ERROR"):
				resp = HTTPResponse(
				"HTTP/1.1", 200, "OK", Headers(Content_Type="image/png"), "helloworld")
                		with open(imagequerycacheresult, 'r') as f:
             				payload = f.read()
             				resp.content = payload
             				resp.headers["Content-Length"] = str(len(payload))
					resp.headers["Access-Control-Allow-Origin"] = "*"
                       			print len(payload)
                        		f.close()
                		flow.reply(resp)
                		return
                	else:	
                		time.sleep(1);
    z = re.match("^/geoserver/z/([\d]+)/([\d]+)/([\d]+)$", flow.request.path)
    if z is not None:
        vectorname = flow.request.path_components[1] + '_' +  flow.request.path_components[2] + '_' + flow.request.path_components[3] + '_' + flow.request.path_components[4]
        vectorquerycache = "/tmp/ramdisk0/accesscache " + vectorname;
	vectorquerycacheresult = os.popen(vectorquerycache).read();
        if (vectorquerycacheresult != "No" and vectorquerycacheresult != "ERROR"):
        	resp = HTTPResponse(
		"HTTP/1.1", 200, "OK", Headers(Content_Type="application/octet-stream"), "helloworld")
                with open(vectorquerycacheresult, 'r') as f:
             		payload = f.read()
             		resp.content = payload
             		resp.headers["Content-Length"] = str(len(payload))
			resp.headers["Access-Control-Allow-Origin"] = "*"
                        resp.headers["Cache-Control"]= "public, max-age=86400"
                        print len(payload)
                        f.close()
                flow.reply(resp)
                return
        else:
                waitingcomm = "/tmp/ramdisk0/waiting " + vectorname;
                os.system(waitingcomm);
        	vectorquerycacheresult = os.popen(vectorquerycache).read();
                print "vectorquerycacheresult: " + vectorquerycacheresult;
                if (vectorquerycacheresult != "No" and vectorquerycacheresult != "ERROR"):
        		resp = HTTPResponse(
			"HTTP/1.1", 200, "OK", Headers(Content_Type="application/octet-stream"), "helloworld")
                	with open(vectorquerycacheresult, 'r') as f:
             			payload = f.read()
             			resp.content = payload
             			resp.headers["Content-Length"] = str(len(payload))
				resp.headers["Access-Control-Allow-Origin"] = "*"
                                resp.headers["Cache-Control"]= "public, max-age=86400"
                        	print len(payload)
                        	f.close()
                	flow.reply(resp)
                        return
    v = re.match("^/geoserver/v/([\d]+)/([\d]+)/([\d]+)$", flow.request.path)
    if v is not None:
        vectorname = flow.request.path_components[1] + '_' +  flow.request.path_components[2] + '_' + flow.request.path_components[3] + '_' + flow.request.path_components[4]
        print "vectorname: " + vectorname;
        vectorquerycache = "/tmp/ramdisk0/accesscache " + vectorname;
	vectorquerycacheresult = os.popen(vectorquerycache).read();
        if (vectorquerycacheresult != "No" and vectorquerycacheresult != "ERROR"):
        	resp = HTTPResponse(
		"HTTP/1.1", 200, "OK", Headers(Content_Type="application/json"), "helloworld")
                with open(vectorquerycacheresult, 'r') as f:
             		payload = f.read()
             		resp.content = payload
             		resp.headers["Content-Length"] = str(len(payload))
			resp.headers["Access-Control-Allow-Origin"] = "*"
                        resp.headers["Cache-Control"]= "public, max-age=86400"
                        print len(payload)
                        f.close()
                flow.reply(resp)
                return
        else:
                waitingcomm = "/tmp/ramdisk0/waiting " + vectorname;
                os.system(waitingcomm);
        	vectorquerycacheresult = os.popen(vectorquerycache).read();
                if (vectorquerycacheresult != "No" and vectorquerycacheresult != "ERROR"):
        		resp = HTTPResponse(
			"HTTP/1.1", 200, "OK", Headers(Content_Type="application/json"), "helloworld")
                	with open(vectorquerycacheresult, 'r') as f:
             			payload = f.read()
             			resp.content = payload
             			resp.headers["Content-Length"] = str(len(payload))
				resp.headers["Access-Control-Allow-Origin"] = "*"
                                resp.headers["Cache-Control"]= "public, max-age=86400"
                        	print len(payload)
                        	f.close()
                	flow.reply(resp)
                	return
    resp = HTTPResponse(
		"HTTP/1.1", 404, "Not Found", Headers(Content_Type="text/html"), "Not Found")
    resp.headers["Content-Length"] = str(len("Not Found"))
    flow.reply(resp)

