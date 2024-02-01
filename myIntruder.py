import requests

cookieHeaders = ['Cookie']
headers = ['Cookie','Origin','Cache-Control','Content-Length','Content-Type','Host','Set-Cookies','Sec-Ch-Ua','Sec-Ch-Ua-Mobile','Sec-Ch-Ua-Platform','Upgrade-Insecure-Requests','User-Agent','Accept','Sec-Gpc','Accept-Language','Accept-Language','Sec-Fetch-Mode','Sec-Fetch-User','Sec-Fetch-Dest','Sec-Fetch-Site','Referer','Accept-Encoding']
requestTypes = ['GET','POST']

class MyIntruder():

    def __init__(self, filename, debug=False):
        self.attributes = {} 
        self.queryParameters = {}
        self.data = {}
        self.headers = {}
        self.cookies = {}
        self.debug=debug
        self.parseRequest(filename)
                
    def parseRequest(self, filename):
        req = ""
        with open(filename, 'r') as file:
            lines = file.readlines()
            i = 0

            for line in lines:
                if(line == '\n'):
                    self.parseData(lines[i+1:])
                    break
                elements = line.replace('\n', '').split(' ')
                headerName = elements[0].replace(':', '')
                if(headerName in requestTypes):
                    content = elements[1]
                    self.attributes['Method'] = headerName
                    queryAttributes = content.split('?')
                    self.attributes['Path'] = queryAttributes[0]
                    if (len(queryAttributes) > 1):
                        for param in queryAttributes[1].split('&'):
                            [name,value] = param.split('=')
                            self.queryParameters[name] = value

                elif(headerName in headers):
                    content = ' '.join(elements[1:])
                    self.headers[headerName] = content
                    if(headerName in cookieHeaders):
                        self.cookies[headerName] = content
                
                else:
                    print('Unknown',headerName)
                i += 1
            if (self.debug):
                print(self.attributes)
                print(self.queryParameters)
                print(self.data)
                print(self.headers)
                print(self.cookies)
    
    def parseData(self,data):
        values = data[0].split('&')
        for value in values:
            [key, val] = value.split('=')
            self.data[key] = val

    def sendRequest(self):
        url = 'https://'+self.headers['Host']+self.attributes['Path']
        if(self.queryParameters != {}):
            url += '?'
            for key,value in self.queryParameters.items():
                url+=key+'='+value
        response = None
        if (self.debug):
            print('URL:',url)
        if(self.attributes['Method'] == "GET"):
            response = requests.get(url=url, data=self.data, headers=self.headers)
        if(self.attributes['Method'] == "POST"):
            response = requests.post(url=url, data=self.data, headers=self.headers)

        return response

    def checkResponse(self, response, value):
        return (response.text.find(value) > 0)

if __name__ == '__main__':
    myintruder = MyIntruder('req.txt', True)
    response = myintruder.sendRequest()
    print(myintruder.checkResponse(response, 'Welcome'))

