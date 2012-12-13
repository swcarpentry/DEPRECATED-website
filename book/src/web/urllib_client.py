import urllib2
instream = urllib2.urlopen("http://software-carpentry.org/testpage.html")
data = instream.read()
instream.close()
print data
