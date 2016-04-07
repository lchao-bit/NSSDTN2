from mitmproxy.models import HTTPResponse
from netlib.http import Headers

import os
import re
import time
import sys
import subprocess
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
                return
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
                return
    v = re.match("^/geoserver/v/([\d]+)/([\d]+)/([\d]+)$", flow.request.path)
    if v is not None:
        vectorname = flow.request.path_components[1] + '_' +  flow.request.path_components[2] + '_' + flow.request.path_components[3] + '_' + flow.request.path_components[4]
        vectorfilepath = "/home/dtn2/bpqrecv/" + vectorname
        ty=flow.request.path_components[1]
        z=flow.request.path_components[2]
        x=flow.request.path_components[3]
        y=flow.request.path_components[4]
        print vectorfilepath
        filename1 = ty + "_" + str(int(z)+1) + "_" + str(int(x)*2) + "_" + str(int(y)*2)
        filename2 = ty + "_" + str(int(z)+1) + "_" + str(int(x)*2+1) + "_" + str(int(y)*2)
        filename3 = ty + "_" + str(int(z)+1) + "_" + str(int(x)*2) + "_" + str(int(y)*2+1)
        filename4 = ty + "_" + str(int(z)+1) + "_" + str(int(x)*2+1) + "_" + str(int(y)*2+1)
        fullpath1 = "/home/dtn2/bpqrecv/" + filename1
        fullpath2 = "/home/dtn2/bpqrecv/" + filename2
        fullpath3 = "/home/dtn2/bpqrecv/" + filename3
        fullpath4 = "/home/dtn2/bpqrecv/" + filename4
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
                return
        elif (os.path.exists(fullpath1) and os.path.exists(fullpath2) and os.path.exists(fullpath3) and os.path.exists(fullpath4)):
        	stage1path = "/home/dtn2/bpqrecv/"+ vectorname + "_" + "1ststage"
  		stage1comm = "jq -s '.[0].features + .[1].features + .[2].features + .[3].features'" + " " + fullpath1 + " " + fullpath2 + " " + " " + fullpath3 + " " + fullpath4 + " " + "> " + stage1path
  		os.system(stage1comm)
  		countrecordcomm = "jq '. |length' " + stage1path
  		countrecord = subprocess.Popen(countrecordcomm, stdout=subprocess.PIPE, shell=True);
  		count = int(countrecord.stdout.read());
  		if(count > 0):
    			stage2path = "/home/dtn2/bpqrecv/"+ vectorname + "_" +"2ndstage"
    			stage2comm = "jq '. | unique_by(.properties.osm_id)'" + " " + stage1path + " > " + stage2path
    			os.system(stage2comm)
    			countrecorduniquecomm = "jq '. |length' " + stage2path         
    			countrecordunique = subprocess.Popen(countrecorduniquecomm, stdout=subprocess.PIPE, shell=True);
    			countunique = int(countrecordunique.stdout.read());
    			stage3path = "/home/dtn2/bpqrecv/"+ vectorname + "_" + "3rdstage"
    			stage3comm = "jq '. | map(select(.properties.minzoom < " + str(int(z)+1) + "))' " + stage2path + " > " + stage3path
    			os.system(stage3comm)
    			stage4path = "/home/dtn2/bpqrecv/"+ vectorname + "_" + "4thstage"
    			source = open(stage3path, "r")
    			target = open(stage4path , "w")
    			lines = source.readlines()
    			target.write("{\"crs\":{\"properties\":{\"name\":\"urn:ogc:def:crs:EPSG::4326\"},\"type\":\"name\"},\"features\":\n");
    			target.writelines(lines)
    			target.write(",\"totalFeatures\":")
    			target.write(str(countunique))
    			target.write(",\"type\":\"FeatureCollection\"}\n")
    			target.close()
    			source.close()
    			formatcomm = "jq -c '.' " + stage4path + " > " + vectorfilepath
    			os.system(formatcomm)
    			del1comm = "rm " + stage1path
    			del2comm = "rm " + stage2path
    			del3comm = "rm " + stage3path
    			del4comm = "rm " + stage4path
                        print del1comm
                        print del2comm
                        print del3comm
    			os.system(del1comm)
    			os.system(del2comm)
    			os.system(del3comm)
    			os.system(del4comm)
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
                        return
  		else:
    			voidcomm = "cp ~/void.json " + vectorfilepath
    			os.system(voidcomm)
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
                        return
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
                return
    resp = HTTPResponse(
		"HTTP/1.1", 404, "Not Found", Headers(Content_Type="text/html"), "Not Found")
    resp.headers["Content-Length"] = str(len("Not Found"))
    flow.reply(resp)
