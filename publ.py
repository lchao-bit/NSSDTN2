#!/usr/bin/python
import sys
import os
import time
name=sys.argv[1]
ty=name.split("_", 1)[0]
na=name.split("_", 1)[1]
sl=na.replace('_', '/')
if ty == "i":
  imageurl="http://166.111.68.197:11193/geoserver/i/" + sl
  imagecomm="curl -o /home/dtn2/respondfile/" + name + " " + imageurl
  pubimage="dtnpublish -s dtn://dtn2.dtn -d dtn://dtne.dtn -p /home/dtn2/respondfile/" + name + " -n " + name
  os.system(imagecomm)
  os.system(pubimage)

elif ty == "v":
  vectorurl="http://166.111.68.197:11193/geoserver/v/" + sl
  vectorcomm="curl -o /home/dtn2/respondfile/" + name + " " + vectorurl
  pubvector="dtnpublish -s dtn://dtn2.dtn -d dtn://dtne.dtn -p /home/dtn2/respondfile/" + name + " -n " + name
  os.system(vectorcomm)
  os.system(pubvector)
  
