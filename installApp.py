import os,sys,string,time,socket
from datetime import date,datetime
from subprocess import Popen, PIPE, STDOUT
from optparse import OptionParser

def RunUDIDDetect(srcRoot):
    proc = Popen([srcRoot + "/tools/udidetect"], stderr=PIPE, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    proc.wait()
    udid = proc.stdout.read(128).strip()
    return udid

def RunFruitStrap(srcRoot, deviceID, uninstall, bundleID, appBundle, appData):
    if uninstall:
        proc = Popen([srcRoot + "/tools/fruitstrap", 'uninstall', '--id=' + deviceID, '--bundle-id=' + bundleID])
        proc.wait()
    proc = Popen([srcRoot + "/tools/fruitstrap", 'install', '--id=' + deviceID, '--bundle=' + appBundle])
    proc.wait()

    xcappdata = appData + "/AppData/"
    trimLen = len(xcappdata)-1
    for root, dirs, files in os.walk(xcappdata):
        for name in files:
            p = root + "/" + name
            rp = p[trimLen:]
            print "Uploading '%s'" % rp
            proc = Popen([srcRoot + "/tools/fruitstrap", 'upload', '--id=' + deviceID, '--bundle-id=' + bundleID, '--file=' + p, '--target=' + rp])
            proc.wait()

parser = OptionParser()
parser.add_option("-s", "--src-root", dest="srcRoot")
parser.add_option("-a", "--app-bundle", dest="appBundle")
parser.add_option("-b", "--bundle-id", dest="bundleID")
parser.add_option("-x", "--xcappdata", dest="appData")
parser.add_option("-d", "--simulator", dest="useSimulator")
parser.add_option("-u", "--uninstall", dest="uninstall", action="store_true", default=False)
(options, args) = parser.parse_args()

deviceID = RunUDIDDetect(options.srcRoot)
RunFruitStrap(options.srcRoot, deviceID, options.uninstall, options.bundleID, options.appBundle, options.appData)
