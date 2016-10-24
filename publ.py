#!/usr/bin/python
import sys
import os
import time
name=sys.argv[1]
ty=name.split("_", 1)[0]
na=name.split("_", 1)[1]
sl=na.replace('_', '/')
if ty == "i":
  imageurl="http://192.168.2.119/geoserver/i/" + sl
  imagecomm="curl -o /home/root/respondfile/" + name + " " + imageurl
  pubimage="/home/root/DTN2/apps/dtnpublish/dtnpublish -s dtn://dtn2.dtn -d dtn://dtne.dtn -p /home/root/respondfile/" + name + " -n " + name
  delimage="rm " + "/home/root/respondfile/" + name
  os.system(imagecomm)
  os.system(pubimage)
  os.system(delimage)

elif ty == "z":
  vectorurl="http://192.168.2.119/geoserver/z/" + sl
  vectorcomm="curl -o /tmp/ramdisk0/respondfile/" + name + " " + vectorurl;
  pubvector="/home/root/DTN2/apps/dtnpublish/dtnpublish -s dtn://dtn2.dtn -d dtn://dtne.dtn -p /tmp/ramdisk0/respondfile/" + name + " -n " + name
  delvector="rm " + "/tmp/ramdisk0/respondfile/" + name
  os.system(vectorcomm)
  os.system(pubvector)
  os.system(delvector)
elif ty == "v":
  vectorurl="http://192.168.2.119/geoserver/v/" + sl
  vectorcomm="curl -o /tmp/ramdisk0/respondfile/" + name + " " + vectorurl;
  pubvector="/home/root/DTN2/apps/dtnpublish/dtnpublish -s dtn://dtn2.dtn -d dtn://dtne.dtn -p /tmp/ramdisk0/respondfile/" + name + " -n " + name
  delvector="rm " + "/tmp/ramdisk0/respondfile/" + name
  os.system(vectorcomm)
  os.system(pubvector)
  os.system(delvector)
