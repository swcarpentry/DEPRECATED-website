import requests
response = requests.get("http://software-carpentry.org/testpage.html")
print 'status code:', response.status_code
print 'content length:', response.headers['content-length']
print response.text
