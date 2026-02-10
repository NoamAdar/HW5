import json

class JSONFileException(Exception):
    pass

class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.originalWheels = wheels.copy()
        self.hash_map = hash_map.copy()
        self.wheels = wheels.copy()
        self.reflector_map = reflector_map.copy()
    

    def encrypt(self, message):
        counter = 0
        encryptMsg = ""

        realEncryptedCnt = [0] 
        # I Saved the counter as a list because I want to change it in other function scope
        for c in message:

            encryptMsg += self.charEncrypt(c,cnt = realEncryptedCnt)
            self.changeWheels(realEncryptedCnt[0])
        #Reset Wheels
        self.wheels = self.originalWheels.copy()

        return "".join(encryptMsg)

    def charEncrypt(self, c, cnt):
        if c.islower() == True:
            cnt[0] += 1
            #stage 1
            i = self.hash_map[c]
        
            #Stage 2

            wheelsValue = self.getWheelsValue()

            if wheelsValue != 0:
                i += wheelsValue
            else:
                i+=1

            #Stage 3

            i = i%26

            #4

            for key, value in self.hash_map.items():
                if value == i:
                    c1 = key

            #5 
            c2 = self.reflector_map[c1]
            #6
            i = self.hash_map[c2]
            #7
            if (wheelsValue != 0):
                i -= wheelsValue
            else:
                i-=1

            #8 
            i = i%26
            #9

            for key, value in self.hash_map.items():
                if value == i:
                    c3 = key

            return c3
        else: 
            return c
        

        
    def getWheelsValue(self):
        return (((2*self.wheels[0]) - self.wheels[1] + self.wheels[2])%26)
    
    def changeWheels(self,counter):
        #W1
        self.wheels[0] += 1
        if self.wheels[0] > 8 :
            self.wheels[0] = 1
        #W2
        if counter%2 == 0 :
            self.wheels[1] *=2
        else:
            self.wheels[1] -=1
        #W3
        if counter%10 == 0 :
            self.wheels[2] = 10
        elif counter%3 == 0:
            self.wheels[2] = 5
        else:
            self.wheels[2] = 0
    

def load_enigma_from_path(path):
    try:
        with open(path,'r') as file:
            dir = json.load(file)
        return Enigma(dir['hash_map'],dir['wheels'],dir['reflector_map'])
    except:
        raise JSONFileException()
        
    
